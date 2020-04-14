
from . import AbstractStateHandler
from app import log
from app.model import booking, car, makemodel, bodytype, user
from app import config
from datetime import datetime
from app.utils import send_email

logger = log.get_logger()
SERVICE_TYPE = 'free'

STATE_ORDER = {
    # renter book a vehicle
    AbstractStateHandler.BOOKING_PHASE_INITIALIZED: 1,

    # admin accepted the deal with renter
    AbstractStateHandler.BOOKING_PHASE_ACCEPTED: 2,

    # admin rejected the deal after discussion
    AbstractStateHandler.BOOKING_PHASE_REJECTED: 2,

    # client cancel after booking initialized, admin cancel after accepting
    AbstractStateHandler.BOOKING_PHASE_CANCELED: 3,

    # renter gave vehicle back to admin, both side give feed back to each other
    AbstractStateHandler.BOOKING_PHASE_DONE: 4
}


def validate_status(status):
    if status not in STATE_ORDER:
        raise Exception('{} is not a valid'.format(status))


class InitializedStateHandler(AbstractStateHandler):
    def handle(self, **kwargs):
        logger.info('{} InitializedStateHandler'.format(SERVICE_TYPE))

        car_id = kwargs['car_id']
        user_id = kwargs['user_id']
        dt_range_from = kwargs['dt_range_from']
        dt_range_to = kwargs['dt_range_to']
        total_price = kwargs['total_price']

        # check if booking user has phone or id info
        user = User.objects(id=user_id).first()
        if (not user.id_number) and (not user.phone_number):
            raise Exception(
                "Either id_number or phone_number can't be empty"
            )

        # check total unfinished trip < max num trips from config
        unfinished_trips = Booking.objects(
            __raw__={
                "renteruser": {"$eq": user_id},
                "current_phase": {
                    "$nin": [
                        AbstractStateHandler.BOOKING_PHASE_DONE,
                        AbstractStateHandler.BOOKING_PHASE_REJECTED,
                        AbstractStateHandler.BOOKING_PHASE_CANCELED,
                    ]
                }
            }
        )

        if len(unfinished_trips) >= int(config.MAXIMUM_UNFINISHED_TRIPS):
            raise Exception(
                "User {} reach maximum of unfinished trips".
                format(user.name)
            )

        # check if vehicle existed
        car = Car.objects(id=car_id).first()
        if not isinstance(car, Car):
            raise Exception(
                "Vehicle id {} "
                "is not existed".format(car_id)
            )

        if car.admin == user_id:
            raise Exception(
                "Renter {} can't book his/her vehicle_id {}".format(
                    user.name, car_id
                )
            )

        if dt_range_from >= dt_range_to:
            raise Exception("date_time range is not valid")

        # if all fine, insert into booking collection with phase = init
        # check if reserved_date_time is available for this vehicle
        # todo: this can be improved
        # todo: by using __raw__ query same as search handler
        for item in car.reserved_list:
            if (item['from'] <= dt_range_from <= item['to']) or \
                    (item['from'] <= dt_range_to <= item['to']):
                raise Exception("Booking date has been reserved")

        booking = Booking()
        booking.user = user_id
        booking.admin = car.admin

        # only show vehicle image
        images = [
            image for image in car.images
            if 'bodytype' in image and
               image['bodytype'] == config.CAR_IMAGE_BODYTYPE
        ]

        booking.car = {
            "id": car_id,
            "images": images,
            "car": car.makemodel,
            "type": car.bodytype,
           
        }
        booking.phases[AbstractStateHandler.BOOKING_PHASE_INITIALIZED] = {
            "date_time": datetime.now().timestamp()
        }

        booking.current_phase = AbstractStateHandler. \
            BOOKING_PHASE_INITIALIZED
        booking.reserved_date_time = {
            "from": dt_range_from,
            "to": dt_range_to
        }
        # fixme, TODO, calculate by server side,
        # todo, then compare with the price send from client
        booking.total_price = float(total_price)
        booking.save()

        # TODO booking status changed to initialized - IMPROVE LATER
        # can use publishing (observers design patterns here)
        # send email to renter
        send_email(
            to_email=user.email,
            # todo localization
            subject="A request to rent a car {} has been submitted".format(booking.car_id),
            # todo localization
            content="Please wait for a response from the company!"
        )
        # send email to admin
        admin = User.objects(id=booking.admin).first()

        send_email(
            to_email=admin.email,
            # todo localization
            subject="Car rental required {}".format(booking.car_id),
            # todo localization
            content="Car hire is required {} from {}".format(
                car.makemodel,
                user.name
            )
        )

        return booking


class AcceptedStateHandler(AbstractStateHandler):
    def handle(self, **kwargs):
        logger.info('{} AcceptedStateHandler'.format(SERVICE_TYPE))

        req_user_id = kwargs['req_user_id']
        booking_id = kwargs['booking_id']
        status = kwargs['status']

        validate_status(status)

        booking_info = Booking.objects.get(car_id=booking_id)

        # check ìf current user allow to approve this
        car = Car.objects(id=booking_info.car['id']).first()

        if car.admin != req_user_id:
            raise Exception(
                "Only the company can accept the booking request"
            )

        if status in booking_info.phases:
            raise Exception('Status {} already set'.format(status))

        if booking_info.current_phase == \
                AbstractStateHandler.BOOKING_PHASE_REJECTED:
            raise Exception(
                "Can't accept after rejected the booking"
            )

        booking_info.current_phase = status
        booking_info.phases[status] = {
            "date_time": datetime.now().timestamp()
        }
        booking_info.save()

        user = User.objects(id=booking_info.user).first()
        admin = User.objects(id=booking_info.admin).first()

        # send email to renter
        send_email(
            to_email=user.email,
            # todo localize
            subject="A request to rent the car {} has been agreed".
            format(booking_info.car_id),
            # todo localize
            content="You can contact us by phone: {} "
                    "or email".format(admin.phone_number, admin.email)
        )
        # send email to admin
        send_email(
            to_email=admin.email,
            # todo localize
            subject="Agree to rent the trip {} successfully".
            format(booking_info.car_id),
            content="You can contact the tenant via phone number: {} "
                    "or email: {}".format(user.phone_number, user.email)
        )
        # update vehicle reserved_list
        car = Car.objects.get(id=booking_info.car['id'])
        if booking_info.reserved_date_time not in vehicle.reserved_list:
            vehicle.reserved_list.append(booking_info.reserved_date_time)
            vehicle.save()

        return booking_info


class RejectedStateHandler(AbstractStateHandler):
    def handle(self, **kwargs):
        logger.info('{} RejectedStateHandler'.format(SERVICE_TYPE))
        booking_id = kwargs['booking_id']
        status = kwargs['status']
        req_user_id = kwargs['req_user_id']

        validate_status(status)

        booking_info = Booking.objects.get(car_id=booking_id)
        # check ìf current user allow to reject the booking
        vehicle = Vehicle.objects(id=booking_info.car['id']).first()

        if vehicle.admin != req_user_id:
            raise Exception(
                "Only vehicle admin can reject the booking request"
            )

        if status in booking_info.phases:
            raise Exception('Status {} already set'.format(status))

        if booking_info.current_phase == \
                AbstractStateHandler.BOOKING_PHASE_ACCEPTED:
            raise Exception(
                "Can't reject after accepting the booking"
            )

        booking_info.current_phase = status
        booking_info.phases[status] = {
            "date_time": datetime.now().timestamp()
        }
        booking_info.save()

        user = User.objects(id=booking_info.user).first()
        admin = User.objects(id=booking_info.admin).first()

        # send email to renter
        send_email(
            to_email=user.email,
            # todo localize
            subject="Your request to rent a car {} has been denied".
            format(booking_info.car_id),
            content="The request to rent a car {} has been rejected by {}".
            format(booking_info.car_id, admin.email)
        )
        # send email to admin
        send_email(
            to_email=admin.email,
            # todo localize
            subject="You have declined the lease request {}".
            format(booking_info.car_id),
            content="You have declined the lease request {}".
            format(booking_info.car_id),
        )

        return booking_info


class CanceledStateHandler(AbstractStateHandler):
    def handle(self, **kwargs):
        logger.info('{} CanceledStateHandler'.format(SERVICE_TYPE))

        booking_id = kwargs['booking_id']
        status = kwargs['status']
        req_user_id = kwargs['req_user_id']

        validate_status(status)
        booking_info = Booking.objects.get(car_id=booking_id)

        # only renters can cancel their booking
        # todo change req_user_id to renter_id
        if booking_info.user != req_user_id:
            raise Exception(
                "Only users can cancel their own booking"
            )

        if status in booking_info.phases:
            raise Exception('Status {} already set'.format(status))

        # todo - reuse this for admin
        # if booking_info.current_phase != \
        #         AbstractStateHandler.BOOKING_PHASE_ACCEPTED:
        #     raise Exception(
        #         'Need to set status {} before {}'.
        #         format(
        #             AbstractStateHandler.BOOKING_PHASE_ACCEPTED,
        #             status
        #         )
        #     )

        booking_info.current_phase = status
        booking_info.phases[status] = {
            "date_time": datetime.now().timestamp()
        }
        booking_info.save()

        vehicle = Vehicle.objects.get(id=booking_info.car['id'])
        if booking_info.reserved_date_time in vehicle.reserved_list:
            vehicle.reserved_list.remove(booking_info.reserved_date_time)
            vehicle.save()

        user = User.objects(id=booking_info.user).first()
        admin = User.objects(id=booking_info.admin).first()

        # send email to renter
        send_email(
            to_email=user.email,
            # todo localize
            subject="You have canceled the car {}".format(booking_info.car_id),
            content="You have canceled the car {}".format(booking_info.car_id)
        )
        # send email to admin
        send_email(
            to_email=admin.email,
            subject="{} has canceled {}".
            format(user.name, booking_info.car_id),
            content="{} has canceled {}".
            format(user.name, booking_info.car_id)
        )

        return booking_info


class DoneStateHandler(AbstractStateHandler):
    def handle(self, **kwargs):
        logger.info('{} DoneStateHandler'.format(SERVICE_TYPE))

        booking_id = kwargs['booking_id']
        status = kwargs['status']
        validate_status(status)
        booking_info = Booking.objects.get(car_id=booking_id)

        if datetime.now().timestamp() < \
                booking_info.reserved_date_time.get('to') - \
                (config.HOURS_TO_GIVE_VEHICLE_BACK_TO_admin * 3600):
            raise Exception(
                "Done status can only set after the last date of booking"
            )

        if status in booking_info.phases:
            raise Exception('Status {} already set'.format(status))

        if booking_info.current_phase != \
                AbstractStateHandler.BOOKING_PHASE_ACCEPTED:
            raise Exception(
                'Need to set status {} before {}'.
                format(AbstractStateHandler.BOOKING_PHASE_ACCEPTED, status)
            )

        booking_info.current_phase = status
        booking_info.phases[status] = {
            "date_time": datetime.now().timestamp()
        }
        booking_info.save()

        car = Car.objects.get(id=booking_info.car['id'])
        if booking_info.reserved_date_time in car.reserved_list:
            car.reserved_list.remove(booking_info.reserved_date_time)
            car.save()

        user = User.objects(id=booking_info.user).first()
        admin = User.objects(id=booking_info.admin).first()

        # send email to renter
        send_email(
            to_email=user.email,
            # todo localize
            subject="You have completed the trip {}".
            format(booking_info.car_id),
            content="You have completed the trip {}".
            format(booking_info.car_id)
        )
        # send email to admin
        send_email(
            to_email=admin.email,
            # todo localize
            subject="Trip {} completed!".format(booking_info.car_id),
            content="Trip {} completed!".format(booking_info.car_id)
        )

        return booking_info