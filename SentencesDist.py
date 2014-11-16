import copy
import linecache
import itertools

def dist_less1(sentence1,sentence2):
  len1 = len(sentence1)
  len2 = len(sentence2)
  if len1 == len2:
    count = 0
    for (word1,word2) in itertools.izip(sentence1,sentence2):
      if word1 != word2:
        if count: 
          return False
        else:
          count += 1
    return True
  elif (len1 - len2) == 1:
    for (index,word1,word2) in itertools.izip(xrange(0,len2),sentence1,sentence2):
      if word1 != word2:
        break
    if index == len2-1:
      return True     
    for (word1,word2) in itertools.izip(sentence1[index+1:],sentence2[index:]):
      if word1 != word2: 
        return False
    return True
  elif (len2 - len1) == 1:
      for (index,word1,word2) in itertools.izip(xrange(0,len1),sentence1,sentence2):
        if word1 != word2:
          break
      if index == len1-1:
        return True          
      for (word1,word2) in itertools.izip(sentence1[index:],sentence2[index+1:]):
        if word1 != word2: 
          return False
      return True
  else:
    return False
  
def hashfunction(key,base):
  return (key-10)%base

def hashfunction_word(word,base):
  return ((ord(word[0])-97)*(ord(word[-1])-97))%base 

def readlineoflargefile(file,no,lineoffset):
  file.seek(lineoffset[no])
  return file.readline().strip().split()[1:]
  
if __name__ == '__main__':
  
  
  pairs = 0
  base = 101
  base1 = 677
  hash_bucket = [[[[] for __ in range(base1)],[[] for __ in range(base1)]] for _ in range(base)]
  
  context = open('sentences.txt')
  line_offset = []
  offset = 0
  line_no = 0
  for line in context:
    line_offset.append(offset)
    offset += len(line)
    
    line = line.strip().split()[1:]
    words_no = len(line)
    # hash len of sentences
    hash_value = hashfunction(words_no, base)
    # hash first word of sentences
    hash_first_word = hashfunction_word(line[0],base1)
    # hash last word of sentences
    hash_last_word = hashfunction_word(line[-1],base1)    
    hash_bucket[hash_value][0][hash_first_word].append(line_no)
    hash_bucket[hash_value][1][hash_last_word].append(line_no)    
    line_no += 1
    
  context.seek(0) 
  pair_set = set()  
  for i in xrange(line_no - 1):
    line = readlineoflargefile(context, i, line_offset)
    words_no = len(line)
    hash_value = hashfunction(words_no, base)
    h_hash_value = hashfunction(words_no + 1, base)
    l_hash_value = hashfunction(words_no - 1, base)
    hash_first_word = hashfunction_word(line[0],base1)
    hash_last_word = hashfunction_word(line[-1],base1)
    
    search_set = set(hash_bucket[hash_value][0][hash_first_word]) | \
                 set(hash_bucket[hash_value][1][hash_last_word]) | \
                 set(hash_bucket[l_hash_value][0][hash_first_word]) | \
                 set(hash_bucket[l_hash_value][1][hash_last_word]) | \
                 set(hash_bucket[h_hash_value][0][hash_first_word]) | \
                 set(hash_bucket[h_hash_value][1][hash_last_word])
    
     
    for j in search_set:
      if i < j:
        line_j = readlineoflargefile(context, j , line_offset)
        if dist_less1(line, line_j):
          pair_set.add((i,j))
          pairs += 1
          print i,line
          print j,line_j      
  print pairs