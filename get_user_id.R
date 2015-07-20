#data0 <- read.csv("EP_with_age.csv",header=T)
data <- data0
data$uid <- NA
data1 <- data.frame(matrix(nrow=0,ncol=19))
id <- 1
while(dim(data)[1]>0){
	indice <- data$created==data$created[1]&data$birthdate==data$birthdate[1]&data$gender==data$gender[1]
	data$uid[indice] <- id
	data1 <- rbind(data1,data[indice,])
	data <- data[!indice,]
	if(id%%10==0){
		print(paste("%",round(100*dim(data1)[1]/dim(data)[1])))
	}
	id <- id + 1
}