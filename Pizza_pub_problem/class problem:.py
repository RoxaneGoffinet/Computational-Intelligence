class problem:
    def __init__(self, nb_ds, nb_ce, capacity = 2):
        self.nb_ds = nb_ds
        self.nb_ce = nb_ce
        self.ds_pizz = nb_ds
        self.ds_pub = 0
        self.ce_pizz = nb_ce
        self.ce_pub = 0
        self.bike_pos = "PIZZERIA"
        self.origin = "PIZZERIA"
        self.destination = "PUB"
        self.capacity = capacity

    def verify_constraint(self):
        # Allows us to verify that there is always less datasientist than computer science students
        if self.ds_pub == 0 :
            return True
        elif self.ds_pub <= self.ce_pub :
            return True
        else :
            return False
    
    def subsample(self) :
        # return possible subsamples of (capacity) people according to the people present in the place
        if self.capacity ==1 :
            return ["C", "D"]
        if self.capacity == 2:
            return ["CC", "CD", "DD", "C", "D"]
        if self.capacity == 3 :
            return ["CCC","CCD", "CDD", "DDD", "CC", "CD", "DD", "C", "D"]
        if self.capacity ==4:
            return ["CCCC","CCCD", "CCDD", "CDDD", "DDDD", "CCC","CCD", "CDD", "DDD", "CC", "CD", "DD", "C", "D"]
        

        


        
        


