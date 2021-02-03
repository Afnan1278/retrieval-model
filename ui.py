from tkinter import *
import boolean_search
import positional_index_search

def entered(arg):
    query_list = arg.split(" ")
    flag=False
    for word in query_list:
        if word == 'NOT' or word == 'AND' or word == 'OR':
            flag=True
            break

    if(flag):
        postfix = boolean_search.convert_to_postfix(query_list)
        ans = boolean_search.query_eval(postfix)
        Result_Field['text'] = '{}'.format(ans)

    else:
        arg1 = arg.replace(' /', '/')
        answer = positional_index_search.making_query(arg1)
        Result_Field['text'] = '{}'.format(answer)


root = Tk()
root.title('IR System')



master=LabelFrame(root,bg='grey',padx=40,pady=40,width=800,height=800)
master.pack()


title=Label(master,text="IR SYSTEM",font="Times 10 bold")
title.pack(pady=20)


Query_Frame=LabelFrame(master,text="Enter your query",font="Times 10 bold",bg='grey')
Query_Frame.pack(pady=20)


Query_Field=Entry(Query_Frame,width=100,bg="white",fg='black')
Query_Field.pack(pady=20)


b=Button(Query_Frame,text="Enter",command=lambda:entered(Query_Field.get()))
b.pack()


output=LabelFrame(master,text="Output",font="Times 10 bold",width=600,height=50)
output.pack(pady=20)

Result_Field=Label(output,text="",width=200,font="Times 10 bold")
Result_Field.pack()
output.pack_propagate(0)
root.mainloop()