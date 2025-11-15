from fastapi import FastAPI
# import logging
# from pythonjsonlogger import jsonlogger

app = FastAPI(title="Demo FastAPI App", version="1.0.0")


# Logger setup
# log_handler = logging.FileHandler("/app/logs/app.log")
# formatter = jsonlogger.JsonFormatter("%(asctime)s %(name)s %(levelname)s %(message)s")
# log_handler.setFormatter(formatter)

# logging.basicConfig(
#     level=logging.INFO,
#     handlers=[log_handler]
# )

# logger = logging.getLogger(__name__)


@app.get("/")
def root():
    print("root")
    # logger.info("Root endpoint accessed")
    return {"message": "Hoollooo from PIE application"}
