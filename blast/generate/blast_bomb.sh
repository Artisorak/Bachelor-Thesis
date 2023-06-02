mode=ball

echo "running blast_bomb.py"
python3 blast_bomb.py $mode

echo "writing to tipsy"
g++ -o txt2tipsy ../../scripts/txt2tipsy.cpp
./txt2tipsy blast_ic_grid_isentrope_relaxed1600_bomb_$mode

echo "moving temporary files to temporary folder"
mkdir temporary
mv blast_ic_grid_isentrope_relaxed1600_bomb_$mode.txt temporary
mv blast_ic_grid_isentrope_relaxed1600_bomb_$mode.tipsy ../run/
cp blast_ic_grid_isentrope_relaxed1600_bomb_$mode.tipsy ~/EULER/cluster/bachelorthesis/NewSPH/pkdgrav3/run/