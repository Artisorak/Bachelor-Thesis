echo "combining"
python3 sod_combine.py

echo "writing to tipsy"
g++ -o txt2tipsy ../../scripts/txt2tipsy.cpp
./txt2tipsy sod_ic_grid_isentrope_relaxed1600_combined

echo "moving temporary files to temporary folder"
mkdir temporary
mv sod_ic_grid_isentrope_relaxed1600_combined.txt temporary
cp sod_ic_grid_isentrope_relaxed1600_combined.tipsy ../run/
cp sod_ic_grid_isentrope_relaxed1600_combined.tipsy ~/EULER/cluster/bachelorthesis/NewSPH/pkdgrav3/run/