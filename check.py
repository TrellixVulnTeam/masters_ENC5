from KL_Divergence import get_result
import nltk
nltk.download('pukt')
nltk.download('stopwords')
#nltk.download('wordnet')
exit()

print()
#query_doc=input("Enter the doc which you need to check for\n")
#query_doc="orig_taska.txt"
query_doc="d1.txt"
#query_doc="d1.txt"
sorted_d=get_result(query_doc)
#print(final)
#print(sorted(final.items(), key = lambda kv:(kv[1], kv[0]),reverse=True))
#sorted_d=sorted(final.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
print("\nThe Documents in decreasing order of their ranks are\n")
for key,val in sorted_d:
    print(key+"\t\t"+str(val))