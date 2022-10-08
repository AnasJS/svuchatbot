import pypff
import time
from src.svuchatbot_mogodb.client import get_collection
from multiprocessing import Process
import multiprocessing as mp


def work(pst):
    pst.do()


class PST:
    def __init__(self, f_path, db_name, n_cores):
        # mp.set_start_method("spawn", force=True)
        self.path = f_path
        self.db_name = db_name
        self.n_cores = n_cores

    def _range(self, order, length):
        r = int(length / self.n_cores)
        start = order * r
        if order == self.n_cores - 1:
            end = length
        else:
            end = start + r
        return start, end

    def do(self, s, e, folder_index, folder_name, folder):
        # pst = pypff.file()
        # pst.open(self.path)
        # root = pst.get_root_folder()
        # root.get_number_of_sub_items()
        # top_folder = root.get_sub_folder(1)
        col = get_collection(self.db_name, folder_name)
        # folder = top_folder.get_sub_folder(folder_index)
        print(" from {} : Start {}, End {}".format(folder_name, s, e))
        for i in range(s, e):
            try:
                msg = folder.get_sub_message(i)
                document = {
                    "subject": msg.subject,
                    "content": msg.plain_text_body.decode(),
                    "sender": msg.sender_name,
                    "header": msg.transport_headers,
                    "sent_time": msg.delivery_time,
                }
                col.insert_one(document)
            except Exception as e:
                print(e)
                continue

    def __work(self, parent, folder_index, folder_name, folder):
        # folder = parent.get_sub_folder(folder_index)
        messages_count = folder.get_number_of_sub_messages()
        processes = []
        for i in range(self.n_cores):
            s, e = self._range(i, messages_count)
            p = Process(target=self.do, args=(s, e, folder_index, folder_name, folder))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()


    # @staticmethod
    # def read_folder(parent, index):
    #     folder = parent.get_sub_folder(index)
    #     messages_count = folder.get_number_of_sub_messages()
    #     documents = []
    #     for i in range(messages_count):
    #         try:
    #             d = {}
    #             msg = folder.get_sub_message(i)
    #             documents.append({
    #                 "subject": msg.subject,
    #                 "content": msg.plain_text_body.decode(),
    #                 "sender": msg.sender_name,
    #                 "header": msg.transport_headers,
    #                 "sent_time": msg.delivery_time,
    #             })
    #         except:
    #             continue
    #     return documents

    def sink(self):
        start_time = time.time()
        pst = pypff.file()
        pst.open(self.path)
        root = pst.get_root_folder()
        root.get_number_of_sub_items()
        top_folder = root.get_sub_folder(1)
        # print(top_folder.label)
        # for f_index, f_name in zip([1, 2, 3, 7, 8], ["Inbox", "Output", "Sent", "Draft", "Junk"]):
        for f_index, f_name in zip([ 3], ["Sent"]):
            print("start sink {}".format(f_name))
            self.__work(top_folder, f_index, f_name, top_folder.get_sub_folder(f_index))
        end_time = time.time()
        work_time = end_time - start_time
        print("The job took " + str(work_time) + " seconds to complete")

