from aiogram import Dispatcher


def setup(dp: Dispatcher):
    """setup filters
    example:
    dp.filter_factory.bind(Filter)
    """
    from app.filters.filters import CallbackDataPrefix, IsSuperUser

    dp.filters_factory.bind(IsSuperUser)
    dp.filters_factory.bind(CallbackDataPrefix)
