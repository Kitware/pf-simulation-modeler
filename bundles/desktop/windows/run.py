import multiprocessing

from pf_sim_2.app.main import main

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main(exec_mode="desktop")
