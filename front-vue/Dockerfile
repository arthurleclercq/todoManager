FROM node:10-alpine            
                           
WORKDIR /front-vue             
ADD . .                   
        
RUN ["npm", "install"]     
                           
EXPOSE 8080                
                           
CMD ["npm", "run", "serve"]
