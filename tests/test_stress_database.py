import threading
import time

from database.database import ClientServerDatabase

if __name__ == '__main__':
    db = ClientServerDatabase('test_database.env', time_limit=10)


    def stress_test():
        users = db.get_list_of_users()
        print(f"len {len(users)}")


    start_time = time.time()
    threads = []

    # while db.db_conn_pool.run:
    for x in range(20):
        thread = threading.Thread(target=stress_test)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time() - start_time
    print(end_time)
    db.close_connections()
