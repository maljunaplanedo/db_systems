mongosh --quiet "clear.js"
./import.sh
mongosh --quiet create.js
mongosh --quiet read1.js > read1_result.txt
mongosh --quiet read2.js > read2_result.txt
mongosh --quiet update.js > update_result.txt
mongosh --quiet delete.js > delete_result.txt
