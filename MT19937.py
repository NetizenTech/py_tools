# /* This library is free software; you can redistribute it and/or   */
# /* modify it under the terms of the GNU Library General Public     */
# /* License as published by the Free Software Foundation; either    */
# /* version 2 of the License, or (at your option) any later         */
# /* version.                                                        */
# /* This library is distributed in the hope that it will be useful, */
# /* but WITHOUT ANY WARRANTY; without even the implied warranty of  */
# /* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.            */
# /* See the GNU Library General Public License for more details.    */
# /* You should have received a copy of the GNU Library General      */
# /* Public License along with this library; if not, write to the    */
# /* Free Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA   */
# /* 02111-1307  USA                                                 */

# /* REFERENCE                                                       */
# /* M. Matsumoto and T. Nishimura,                                  */
# /* "Mersenne Twister: A 623-Dimensionally Equidistributed Uniform  */
# /* Pseudo-Random Number Generator",                                */
# /* ACM Transactions on Modeling and Computer Simulation,           */
# /* Vol. 8, No. 1, January 1998, pp 3--30.                          */

# Period parameters */
N = 624
M = 397
MATRIX_A = 0x9908b0df    # constant vector a */
UPPER_MASK = 0x80000000  # most significant w-r bits */
LOWER_MASK = 0x7fffffff  # least significant r bits */

# Tempering parameters */
TEMPERING_MASK_B = 0x9d2c5680
TEMPERING_MASK_C = 0xefc60000

mt = [0 for _ in range(N)]  # the array for the state vector  */
mti = N+1                   # mti==N+1 means mt[N] is not initialized */


# Initializing the array with a seed
def sgenrand(seed):
    global mt
    global mti
    for i in range(N):
        mt[i] = seed & 0xffff0000
        seed = 69069 * seed + 1
        mt[i] |= (seed & 0xffff0000) >> 16
        seed = 69069 * seed + 1

    mti = N


def genrand():
    global mt
    global mti
    mag01 = [0x0, MATRIX_A]
    # /* mag01[x] = x * MATRIX_A  for x=0,1 */

    if mti >= N:            # /* generate N words at one time */

        if mti == N+1:      # /* if sgenrand() has not been called, */
            sgenrand(4357)  # /* a default initial seed is used   */

        for kk in range(0, N-M):
            y = (mt[kk] & UPPER_MASK) | (mt[kk+1] & LOWER_MASK)
            mt[kk] = mt[kk+M] ^ (y >> 1) ^ mag01[y & 0x1]

        for kk in range(N-M, N-1):
            y = (mt[kk] & UPPER_MASK) | (mt[kk+1] & LOWER_MASK)
            mt[kk] = mt[kk+(M-N)] ^ (y >> 1) ^ mag01[y & 0x1]

        y = (mt[N-1] & UPPER_MASK) | (mt[0] & LOWER_MASK)
        mt[N-1] = mt[M-1] ^ (y >> 1) ^ mag01[y & 0x1]

        mti = 0

    y = mt[mti]
    y ^= (y >> 11)
    y ^= (y << 7) & TEMPERING_MASK_B
    y ^= (y << 15) & TEMPERING_MASK_C
    y ^= (y >> 18)

    mti += 1
    return y


if __name__ == '__main__':
    sgenrand(4357)
    for i in range(1_000):
        print(genrand())
