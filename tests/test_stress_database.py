import threading
import time

from database.database import ClientServerDatabase

if __name__ == '__main__':
    db = ClientServerDatabase('test_database.env', time_limit=30)


    def stress_test():
        users = db.get_list_of_users()
        return users


    start_time = time.time()
    threads = []

    # while db.db_conn_pool.run:
    #     stress_test()
    while db.db_conn_pool.run:
        thread = threading.Thread(target=stress_test)
        time.sleep(0.02)
        threads.append(thread)
        thread.start()

    print(len(threads))
    count = 0
    for thread in threads:

        print(len(threads) - count)
        thread.join()
        count += 1

    end_time = time.time() - start_time
    print(end_time)
    db.close_connections()
