a = [[0], ["2", "9", "4", "2", "10", "10"], ["2", "10", "8", "a"], ["a", "a", "a", "4", "10"]]
ace_count = [0,0,0,0]
final_val = 0

stored_vals = [0,0,0,0]

print("-------------")
for i, j in enumerate(a):
    for k in j:
        if k == "a":
            adding_val = 11
            ace_count[i] += 1
        else:
            adding_val = int(k)
        final_val += adding_val
    
    while final_val > 21:
        if final_val > 21 and ace_count[i] > 0:
            final_val -= 10
            ace_count[i] -= 1
        else:
            print("bust")
            break



    print(f"hand {i}: {final_val}")
    stored_vals[i] = final_val
    final_val = 0
    print(f"ace count {i}: {ace_count}")
    print("-------------")
    
    

print(stored_vals)