import subprocess
print("subprocess - begin")

subprocess.run(["bash", "printArgs.sh", "7789"])

# bash -c "HNC_DIR=$PWD ./printArgs \$1 & disown" -- 7789
subprocess.run(["bash", "-c", "HNC_DIR=$PWD ./printArgs $1 & disown", "--", "7789"])

print("subprocess - end")
