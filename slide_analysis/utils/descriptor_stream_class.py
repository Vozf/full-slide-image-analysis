class DescriptorStream:
    def __init__(self, descriptor_database_read_service):
        self.iteration = 0
        self.descriptor_database_read_service = descriptor_database_read_service
        self.file = open(self.descriptor_database_read_service.path, 'rb')

    def next(self):
        res = self.descriptor_database_read_service._load_obj(self.file)
        self.iteration += 1
        return res

    def has_next(self):
        if self.iteration < len(self):
            return True
        else:
            self.file.close()
            return False

    def __len__(self):
        return len(self.descriptor_database_read_service)

    def for_each(self, func):
        while self.has_next():
            print(str(self.iteration) + '/' + str(len(self)))
            func(self.next())
