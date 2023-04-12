import abc


class Rate(abc.ABC):
    @abc.abstractmethod
    def compute_rate_with_error(self):
        pass

    @abc.abstractmethod
    def plot_rate(self):
        pass
