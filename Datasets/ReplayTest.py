import time

import torch
from torch.utils.data import Dataset
from torch.utils.data.dataloader import DataLoader
from torch import multiprocessing as mp


class SimpleDataset(Dataset):
    def __init__(self, data, device, queue):
        self.data = data
        self.device = device
        self.queue = queue

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data = self.data[idx]
        if self.device == 'cuda':
            data.to(self.device).share_memory_()
        self.queue.put(data)


"""
When both batch_size and batch_sampler are None (default value for batch_sampler is already None), 
automatic batching is disabled. Each sample obtained from the dataset is processed with the function passed as the 
collate_fn argument.

When automatic batching is disabled, the default collate_fn simply converts NumPy arrays into PyTorch Tensors, and 
keeps everything else untouched.
"""


class RandomSampler:
    r"""Samples elements randomly. If without replacement, then sample from a shuffled dataset.
    If with replacement, then user can specify :attr:`num_samples` to draw.

    Args:
        data_source (Dataset): dataset to sample from
        replacement (bool): samples are drawn on-demand with replacement if ``True``, default=``False``
        num_samples (int): number of samples to draw, default=`len(dataset)`.
        generator (Generator): Generator used in sampling.
    """
    def __init__(self, data_source, replacement, num_samples, generator=None):
        self.data_source = data_source
        self.replacement = replacement
        self._num_samples = num_samples
        self.generator = generator

        if not isinstance(self.replacement, bool):
            raise TypeError("replacement should be a boolean value, but got "
                            "replacement={}".format(self.replacement))

        if not isinstance(self.num_samples, int) or self.num_samples <= 0:
            raise ValueError("num_samples should be a positive integer "
                             "value, but got num_samples={}".format(self.num_samples))

    @property
    def num_samples(self):
        # dataset size might change at runtime
        if self._num_samples is None:
            return len(self.data_source)
        return self._num_samples

    def __iter__(self):
        n = len(self.data_source)
        if self.generator is None:
            seed = int(torch.empty((), dtype=torch.int64).random_().item())
            generator = torch.Generator()
            generator.manual_seed(seed)
        else:
            generator = self.generator

        if self.replacement:
            for _ in range(self.num_samples // 32):
                yield from torch.randint(high=n, size=(32,), dtype=torch.int64, generator=generator).tolist()
            yield from torch.randint(high=n, size=(self.num_samples % 32,), dtype=torch.int64, generator=generator).tolist()
        else:
            for _ in range(self.num_samples // n):
                yield from torch.randperm(n, generator=generator).tolist()
            yield from torch.randperm(n, generator=generator).tolist()[:self.num_samples % n]

    def __len__(self):
        return self.num_samples


class ReplayDataLoader:
    def __init__(self, data, device):
        self.data = data
        self.device = device

        # Launch N workers
        # Each adds gpu (or cpu if no cuda) data to a queue
        # Up to prefetch factor
        # Based on sampler - somehow consistent per worker

        # Launch a thread to collate here in a list
        # Pop from that list

        # Main worker also does the function, in a thread, and controls the lock to release/acquire when next

        # Can add non-gpu Queue items to pre-allocated pinned memory up to specified index (if gpu)
        # gpu items can be stacked later with pinned memory

        """
        The collate function has access to Batches; a tape of pinned memory (batch_size * prefetch_factor, 
        for each key (and batch size?) encountered (recently?).
        
        Therefore workers must be spawned to avoid pickling error? Collate class
        
        Batches stacks gpu and pinned memory.cuda() when called.
        """

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data = self.data[idx]
        return data


class SimpleDataset2(Dataset):
    def __init__(self, data, device):
        self.data = data
        self.device = device

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data = self.data[idx]
        return data


class SimpleDataset3(Dataset):
    def __init__(self, data, device, queue):
        self.data = data
        self.device = device
        self.queue = queue

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data = self.data[idx]
        self.queue.put(data.cuda(non_blocking=True).share_memory_())


def run():
    d = torch.rand(1000, 50, 2)
    queue = mp.Queue()
    dataset = SimpleDataset3(d, 'cuda', queue)
    dataloader = DataLoader(dataset, batch_size=32, num_workers=8, collate_fn=Collate(queue))
    print(next(iter(dataloader)).shape)
    # while not prefetch_queue.empty():
    #     print(next(iter(dataloader)).shape)


class Collate:  # Can have a pinned memory buffer and jitted parallel/threaded? writes? trace?
    # https://gist.github.com/rossant/7a46c18601a2577ac527f958dd4e452f

    # Make 3 shared memory prefetch batches
    # Write to them from workers using shared ... maybe each worker gets all batch elemts and just does its chunk?
    #   Then shared prefetch index 1,2,3
    #         Sharable np array 4 x 256 x ...
    #         Sharable list or tensor indexing the 256 dimension
    #         Every batch added may allocate a new datum, and a link is added to the manager dict that gets cached by w
    # Collate  pins - does as_tensor work on un-copied shared?

    # If shared cuda can be written, can sendsampler index for pre-allocated prefetch cuda tensor; Collate can just
    # return the corresponding prefetch (based on a normal-shared variable with sampler)
    #       Via numpy but collate can send prefetch index i to cuda and the rest to pin, incrementing i as the one after
    #       the sampler/collate variable one - i gets sent - workers can send index if gpu else none; i can stack

    def __init__(self, queue=None):
        self.queue = queue

    def __call__(self, x):
        if self.queue is None:
            return torch.stack(x)
        return self.queue.get()
        # return torch.stack([self.queue.get() for _ in range(32) if not self.queue.empty()])


class Worker:
    def __init__(self):
        self.t = torch.ones([2, 2])

    def __call__(self, i):
        if i == 0:
            self.t = 2
        else:
            time.sleep(2)
        print(self.t, i)

    def __setitem__(self, ind, value):
        print(ind)
        if self.t.shape:
            self.t[ind] = value
        else:
            self.t[...] = value
        print(self.t)

    def __iter__(self):
        return self

    def __next__(self):
        return 5


if __name__ == '__main__':
    torch.multiprocessing.set_start_method('spawn')
    # run()
    # print(timeit.timeit(run, number=1))
    worker = Worker()
    # for i in range(2):
    #     mp.Process(target=worker, args=(i,)).start()
    # for x in worker:
    #     print(x)
    worker[...] = 5