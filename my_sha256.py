import hashlib

'''
    循环右移运算
    参数: x:整型，运算数; n:整型，右移位数
    返回：整型
'''
def rrm(x, n):
    bin_x = '{:032b}'.format(x)
    adt = bin_x[-n:]
    res = adt + bin_x[:-n]
    return int(res,base=2)

'''
    扩展消息快
'''
def expandM(m):
    sg0 = lambda x : (rrm(x,7) ^ rrm(x,18) ^ (x>>3))
    sg1 = lambda x : (rrm(x,17) ^ rrm(x,19) ^ (x>>10))
    w = [int(m[j:j+8], base=16) for j in range(0, 128, 8)]
    for j in range(512//32, 64):
        e1,e2,e3,e4 = sg1(w[j-2]),w[j-7],sg0(w[j-15]),w[j-16]
        w.append((e1 + e2 + e3 + e4) % (2**32))
    return w
        
# 初始哈希值，取自自然数前八个质数的平方根的小数部分前32位
H = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
# 64个常数，取自自然数中前面64个素数的立方根的小数部分的前32位
K = [
   0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
   0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
   0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
   0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
   0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
   0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
   0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
   0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]
# 加法的模值
mod = 2**32
# 原始消息
raw_data = ('白日依山尽，黄河入海流').encode('utf-8')

# 消息预处理，在消息后面进行补码操作
data = raw_data.hex()
l = '{:016x}'.format(len(data*4))
zero_nums = (448-((len(data)*4)%512+1)) % 512
block_nums = zero_nums // 8
data1 = data + '80' + '00'*block_nums + l

# 将补码完的消息进行切块，每个块长度为512bit
N = len(data1) // 128
M = [data1[i:i+128] for i in range(0,len(data1),128)]

# 定义逻辑函数
Ch = lambda x,y,z : (x&y) ^ ((~x)&z)
M_aj = lambda x,y,z: (x&y) ^ (x&z) ^ (y&z)
Sig0 = lambda x: rrm(x,2) ^ rrm(x,13) ^ rrm(x,22)
Sig1 = lambda x: rrm(x,6) ^ rrm(x,11) ^ rrm(x,25)

# 遍历每个数据块
for i in range(N):
    # 分割并扩展数据块，每个切片长度为32bit，共有64个切片
    W = expandM(M[i])
    parm = H.copy()
    for j in range(64):
        S1 = Sig1(parm[4])
        ch =Ch(parm[4], parm[5], parm[6])
        T1 = (parm[-1] + S1 + ch + K[j] + W[j]) % mod
        T2 = (Sig0(parm[0]) + M_aj(parm[0], parm[1], parm[2])) % mod
        parm[-1] = parm[-2]
        parm[-2] = parm[-3]
        parm[-3] = parm[-4]
        parm[-4] = (parm[-5] + T1) % mod
        parm[-5] = parm[-6]
        parm[-6] = parm[-7]
        parm[-7] = parm[-8]
        parm[-8] = (T1 + T2) % mod
    H = [(i+j) % mod for i,j in zip(H, parm)]
    
my_hash = ''          
for h in H:
    my_hash += '{:08x}'.format(h)

print(my_hash)

# data = 'BlockChain'.encode('utf-8')
# data_bin = data.hex()

digest = hashlib.sha256(raw_data).hexdigest()
print(digest)

print(my_hash==digest)