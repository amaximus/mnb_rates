import json
import logging
import voluptuous as vol
from datetime import datetime
from datetime import timedelta
from mnb import Mnb

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.discovery import async_load_platform

REQUIREMENTS = [ ]

_LOGGER = logging.getLogger(__name__)

CONF_ATTRIBUTION = "Data provided by mnb.hu"
CONF_NAME = 'name'
CONF_CURRENCIES = 'currencies'

DEFAULT_ICON = 'mdi:cash'
DEFAULT_NAME = 'MNB rates'

SCAN_INTERVAL = timedelta(hours=3)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_CURRENCIES, default=[]): vol.All(cv.ensure_list, [cv.string]),
})

async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    name = config.get(CONF_NAME)
    currencies = config.get(CONF_CURRENCIES)

    async_add_devices(
        [MNBCurrenciesSensor(hass, name, currencies)],update_before_add=True)

async def async_get_cdata(self):
    cjson = {}

    client = await self._hass.async_add_executor_job(Mnb)
    p3 = await self._hass.async_add_executor_job(client.get_current_exchange_rates)
    cjson = json.loads(p3.to_json())

    return cjson

async def async_get_cunit(self):
    client = await self._hass.async_add_executor_job(Mnb)
    p3 = await self._hass.async_add_executor_job(client.get_currency_units, self._all_currencies)

    currencies_result = {}
    for currency_unit in p3:
        currencies_result.update({currency_unit.currency : currency_unit.unit})
    _LOGGER.debug(str(currencies_result))

    return currencies_result

async def async_get_currencies(self):
    client = await self._hass.async_add_executor_job(Mnb)
    p3 = await self._hass.async_add_executor_job(client.get_currencies)

    return p3

class MNBCurrenciesSensor(Entity):

    def __init__(self, hass, name, currencies ):
        """Initialize the sensor."""
        self._hass = hass
        self._name = name
        self._state = 0
        self._last_poll = ""
        self._cdata = []
        self._cunit = []
        self._allcurrencies = []
        self._currencies = currencies
        self._currency = None
        self._cunit1 = None
        self._icon = DEFAULT_ICON

    @property
    def extra_state_attributes(self):
        attr = {"rates": []}

        if 'rates' in self._cdata:
            if len(self._currencies) == 1:
                attr["currency"] = self._currency
                attr["unit"] = self._cunit1
            else:
                for item in self._cdata['rates']:
                    if len(self._currencies) > 0:
                         if item.get('currency') not in self._currencies:
                             continue
                    _LOGGER.debug("found: " + item.get('currency') + ": " + str(item.get('rate')))
                    attr['rates'].append({"currency": item.get('currency'),"rate": item.get('rate'), "unit": self._cunit.get(item.get('currency'))})

        attr["provider"] = CONF_ATTRIBUTION
        attr["last_poll"] = self._last_poll
        return attr

    async def async_update(self):

        self._cdata = await async_get_cdata(self)
        if len(self._cdata) == 0:
            self._state = 1
        else:
            self._all_currencies = await async_get_currencies(self)
            _LOGGER.debug(str(self._all_currencies))

            self._cunit = await async_get_cunit(self)
            if len(self._currencies) == 1:
                for item in self._cdata['rates']:
                    if item.get('currency') not in self._currencies:
                        continue
                    self._state = item.get('rate')
                    self._currency = item.get('currency')
                    self._cunit1 = self._cunit.get(item.get('currency'))
                    break

        dt_now = datetime.now()
        self._last_poll = dt_now.strftime("%Y/%m/%d %H:%M")

        return self._state

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return DEFAULT_ICON
