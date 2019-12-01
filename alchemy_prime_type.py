from functools import reduce

from sqlalchemy.types import INT, TypeDecorator

PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, ]  # len(10)


class PrimeHelper(object):
    """Class of prime_type sources for DB with helpers functions."""
    def __init__(self):
        """create helper collections."""
        self.ISO = dict(enumerate(PRIMES, 1))
        self.ISO_REV = self.inverse_mapping(self.ISO)
        self.ALL = reduce(lambda x, y: x * y, PRIMES)

    @staticmethod
    def inverse_mapping(f):
        """return reversed collection."""
        return f.__class__(map(reversed, f.items()))

    @staticmethod
    def prime_products(n):
        """return list of all products of prime numbers list."""
        res = [1]
        for p in n:
            res += [x * p for x in res]
        return sorted(set(res))

    @staticmethod
    def prime_factors(n):
        """generator of prime factors of given number."""
        i = 2
        while i * i <= n:
            if n % i == 0:
                n //= i
                yield i
            else:
                i += 1

        if n > 1:
            yield n


prime_helper = PrimeHelper()


class PrimeType(TypeDecorator):
    """Represents an Prime Integer data type DB.

     prime = db.Column(PrimeType, index=True)

     @classmethod
     def query(cls, query, n):
         if isinstance(n, int):
             query = query.filter(cls.prime.in_(prime_helper.prime_factors(n)))
         return query

      ~5x faster then relation (in very basic test)
     """

    impl = INT

    def process_bind_param(self, value, dialect):
        """Transform list to int (for save)."""
        if value is not None:
            if isinstance(value, list):
                value = reduce(lambda x, y: x * y, [prime_helper.ISO.get(x) for x in filter(
                    lambda z: z in prime_helper.ISO.keys(), value)], 1)
            if not isinstance(value, int) or not 1 < value < prime_helper.ALL:
                value = None
        return value

    def process_result_value(self, value, dialect):
        """Transform int to list (for get)."""
        if value is not None:
            value = sorted([prime_helper.ISO_REV.get(x) for x in filter(
                lambda y: y in prime_helper.ISO_REV.keys(), prime_helper.prime_factors(value))])
        return value
