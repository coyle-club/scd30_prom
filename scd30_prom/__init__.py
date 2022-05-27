from scd30_i2c import SCD30
import click
import time
from prometheus_client import start_http_server, Gauge
import logging


@click.command
@click.option("-i", "--interval", type=int, default=15)
@click.option("-p", "--port", type=int, default=5000)
@click.option("-l", "--label", "labels", type=str, multiple=True)
def main(interval, port, labels):
    logging.basicConfig(level=logging.INFO)
    s = SCD30()

    label_dict = dict([label.split("=") for label in labels])

    co2_gauge = Gauge("scd30_co2", "SCD30 CO2 reading")
    temp_gauge = Gauge("scd30_temp", "SCD30 temperature reading")
    rh_gauge = Gauge("scd30_rh", "SCD30 relative humidity reading")
    last_read_gauge = Gauge("scd30_last_read", "SCD30 last read timestamp")
    start_http_server(port)

    while True:
        try:
            s.set_measurement_interval(interval)
            s.start_periodic_measurement()
            logging.info("SCD30 ready")

            while True:
                if s.get_data_ready():
                    data = s.read_measurement()
                    if data:
                        co2, temp, rh = data
                        co2_gauge.labels(**label_dict).set(co2)
                        temp_gauge.labels(**label_dict).set(temp)
                        rh_gauge.labels(**label_dict).set(rh)
                        last_read_gauge.labels(**label_dict).set(
                            int(time.time() * 1000)
                        )
                    time.sleep(interval)
                else:
                    time.sleep(0.2)
        except OSError as err:
            if err.errno == 121:
                logging.warn("Caught error 121, will retry in %s sec", interval)
                time.sleep(interval)
            else:
                raise err


if __name__ == "__main__":
    main()
