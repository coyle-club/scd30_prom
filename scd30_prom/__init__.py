from scd30_i2c import SCD30
import click
import time
from prometheus_client import start_http_server, Gauge


@click.command
@click.option("--interval", type=int, default=15)
@click.option("--port", type=int, default=5000)
def main(interval, port):
    s = SCD30()
    s.set_measurement_interval(interval)
    s.start_periodic_measurement()

    time.sleep(interval)

    co2_gauge = Gauge("scd30_co2", "SCD30 CO2 reading")
    temp_gauge = Gauge("scd30_temp", "SCD30 temperature reading")
    rh_gauge = Gauge("scd30_rh", "SCD30 relative humidity reading")
    last_read_gauge = Gauge("scd30_last_read", "SCD30 last read timestamp")

    start_http_server(port)

    while True:
        if s.get_data_ready():
            data = s.read_measurement()
            if data:
                co2, temp, rh = data
                co2_gauge.set(co2)
                temp_gauge.set(temp)
                rh_gauge.set(rh)
                last_read_gauge.set(int(time.time() * 1000))
            time.sleep(interval)
        else:
            time.sleep(0.2)


if __name__ == "__main__":
    main()
