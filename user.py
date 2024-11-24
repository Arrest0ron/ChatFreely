
class BaseUser():
    def __init__(self, data):
        self._telegram_uid = data[0]
    
    @property
    def telegram_uid(self):
        return self._telegram_uid

    @telegram_uid.setter
    def telegram_uid(self, uid):
        self._telegram_uid = uid
        
class SearchUser(BaseUser):
    def __init__(self, data):
        self._telegram_uid = data[0]
        self._rating = data[1]

        
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        self._rating = rating
        
class User(SearchUser):
    def __init__(self, data):
        self._telegram_uid = data[0]
        self._user_status = data[1]
        self._rating = data[2]
        self._registration = data[3]
        self._total_connections = data[4]
        self._last_update = data[5]
        self._last_connected = data[6]
        self._reports = data[7]

    @property
    def connected_uid(self):
        return self._connected_uid

    @connected_uid.setter
    def connected_uid(self, uid):
        self._connected_uid = uid

    @property
    def registration(self):
        return self._registration

    @registration.setter
    def registration(self, registration):
        self._registration = registration
        
    
    @property
    def user_status(self):
        return self._user_status

    @user_status.setter
    def user_status(self, status):
        self._user_status = status

    @property
    def last_update(self):
        return self._last_update

    @last_update.setter
    def last_update(self, update):
        self._last_update = update
    
    @property
    def total_connections(self):
        return self._total_connections

    @total_connections.setter
    def total_connections(self, total_connections):
        self._total_connections = total_connections
        
    @property
    def last_connected(self):
        return self._last_connected

    @last_connected.setter
    def last_connected(self, last_connected):
        self._last_connected = last_connected
        
    @property
    def reports(self):
        return self._reports

    @reports.setter
    def reports(self, reports):
        self._reports= reports

class ConnectedUser(BaseUser):
    def __init__(self, data):
        super().__init__(data[0])
        self._telegram_uid = data[1]
      
    @property
    def telegram_uid_2(self):
        return self._telegram_uid

    @telegram_uid_2.setter
    def telegram_uid_2(self, uid):
        self._telegram_uid = uid
        