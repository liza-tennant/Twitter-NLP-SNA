#this script reads a .txt file from the inputs folder and outputs a tagged file of the same name into the outputs folder 

cd ark-tweet-nlp-0.3.2/inputs/RIGHT/

for f in *.txt; do 
    java -Xmx500m -jar ark-tweet-nlp-0.3.2.jar --output-format conll $f > ~/ark-tweet-nlp-0.3.2/outputs_conll/RIGHT/$f;
done 

#NB had to copy .jar file to inputs/LEFT and inputs/RIGHT folders
