from logging import DEBUG, basicConfig, getLogger

basicConfig(
    level=DEBUG, format="%(asctime)s [%(levelname)s] %(module)s:%(lineno)d: %(message)s"
)

logger = getLogger("data-viz-demo")
