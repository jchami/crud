import multiprocessing
import os

bind = "0.0.0.0:{}".format(os.environ.get("PORT", 8000))
workers = multiprocessing.cpu_count() * 2 + 1

