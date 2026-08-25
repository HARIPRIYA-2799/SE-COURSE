#grading system assignment

while True:
    try:
        a=int(input('Enter a number: '))
        print('The value entered is:' ,a)
        if 0<=a<=35:
            print('GRADE D')
        elif 35<a<=60:
            print('GRADE C')
        elif 60<a<=80:
            print('GRADE B')
        elif 80<a<=100:
            print('GRADE A')
        else:
            print("enter numbers between 1 to 100 only")
            break
    except ValueError:
        print("Plese enter a number only")
  
