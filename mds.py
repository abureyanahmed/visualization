import sqlite3
import numpy as np

def get_user_space(rows):
        conn = sqlite3.connect('../uofadata.db')
        authors = conn.execute("SELECT rowid, auid, name, researcharea FROM authorsummary WHERE rowid <= "+sys.argv[1])
        topics = set()
        topics_of_person = list()
        for author in authors:
                research_areas = set()
                for phrase in author[3].split(","):
                        t = phrase.strip().lower()
                        if t != '':
                                research_areas.add(t)
                topics_of_person.append(research_areas)
                for r in research_areas:
                        #if r in topics:print r
                        topics.add(r)
        conn.close()
        n = 0
        index = dict()
        inv_index = list()
        for x in topics:
                inv_index.append(x)
                index[x] = n
                n = n + 1
        user_space = np.zeros(shape=(len(topics_of_person), len(topics)))
        for i in range(len(topics_of_person)):
                for j in range(len(topics)):
                        if inv_index[j] in topics_of_person[i]:
                                user_space[i][j] = 1
                                
        ti = 0
        tj = 0
        for j in range(len(topics)):
                mark1 = False
                mark2 = False
                for i in range(len(topics_of_person)):
                        if user_space[i][j] !=0:
                                if mark1 == False:
                                        mark1 = True
                                else:
                                        mark2 = True
                                if mark1 and mark2:
                                        ti = i
                                        tj = j
                                        break
                if mark1 and mark2:
                        break

        for j in range(len(topics)):
                x = 0
                for i in range(len(topics_of_person)):
                        x = x + user_space[i][j]
                for i in range(len(topics_of_person)):
                        user_space[i][j] = user_space[i][j]/x
        print("user_space")
        print(user_space[ti][tj])

        return user_space, inv_index, index

import math
import matplotlib.pyplot as plt

def mds(M, L, scale=1.0):
        MTM = np.dot(M.T, M)
        #for i in range(MTM.shape[0]):
#                for j in range(MTM.shape[1]):
#                        if MTM[i][j] == 0:
#                                MTM[i][j]=5
#                        else:
#                                MTM[i][j] = 1/MTM[i][j]
        n = MTM.shape[0]
        I = np.zeros(shape=(n, n))
        for i in range(I.shape[0]):
                I[i][i] = 1
        col_one = np.zeros(shape=(n, 1))
        col_one.fill(1)
        row_one = np.zeros(shape=(1, n))
        row_one.fill(1)
        H = I - np.dot(col_one, row_one)/n
        P = -.5 * np.dot(np.dot(H, MTM),H)
        U, s, V = np.linalg.svd(P, full_matrices=True)
        sig = np.zeros(shape=(n, 2))
        sig[0][0] = math.sqrt(s[0]) * scale
        sig[1][1] = math.sqrt(s[1]) * scale
        out_arr = np.dot(U,sig)
        #plt.plot(out_arr[:,0], out_arr[:,1], "o")
	minx = maxx = miny = maxy = 0
	for i in range(out_arr.shape[0]):
		plt.text(out_arr[i][0], out_arr[i][1], L[i])
		if minx > out_arr[i][0]:minx = out_arr[i][0]
		if maxx < out_arr[i][0]:maxx = out_arr[i][0]
		if miny > out_arr[i][1]:miny = out_arr[i][1]
		if maxy < out_arr[i][1]:maxy = out_arr[i][1]
	plt.axis([minx-1, maxx+1, miny-1, maxy+1])
        plt.show()

import sys

def test2():
        test = np.zeros(shape=(25, 2))
        label = list()
        for i in range(5):
                for j in range(5):
                        test[i*5+j][0]=i
                        test[i*5+j][1]=j
                        label.append(str(i*5+j))
        mds(test.T, label)

#test2()


def test1():
        M, L, Ind = get_user_space(sys.argv[1])
        mds(M, L, 10.0)
        print(L)
        MTM2 = np.dot(M.T, M)
        while True:
                print("Get total authors(1), Compare(2) or get total similarity(3):")
                choice = raw_input()
                if choice=="1":
                        print(np.sum(M[:,Ind[raw_input()]]))
                elif choice=="2":
                        topic1 = raw_input()
                        topic2 = raw_input()
                        v1 = M[:,Ind[topic1]]
                        v2 = M[:,Ind[topic2]]
                        print(np.sum([v1[i]*v2[i] for i in range(len(v1))]))
                elif choice=="3":
                        print(np.sum(MTM2[:,Ind[raw_input()]]))

test1()

def test3():
        M = np.zeros(shape=(2, 3))
        M[0][0] = 1
        M[0][1] = 1
        M[0][2] = 0
        M[1][0] = 0
        M[1][1] = 0
        M[1][2] = 1
        L = ["1", "2", "3"]
        mds(M,L)
        
#test3()
