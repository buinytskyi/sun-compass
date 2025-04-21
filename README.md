## Sun Compass
![Image](app/image.png)

This is a proof of concept of how to use sky bodies.</br>
The combination of four dimensions (position on the geoid) and astronomic time,</br> allows to predict the position of the sun and the cardinal direction. 

## Run by OS independent way (Windows, Linux/Unix, MacOS)
### Python environment runtime and execution:
https://wiki.python.org/moin/BeginnersGuide/Download<br />
https://docs.python.org/3/installing/index.html
https://packaging.python.org/en/latest/tutorials/installing-packages/
```
pip install -r requirements.txt
python app/main.py
```

## Run on Android
![Image](app/icon.png)
### How to build Android APK

Run Linux on Microsoft Windows by WSL:
- Install WSL, run CMD or Powershell from Administrator and reboot PC:
```wsl --install -d Ubuntu-22.04```
- Win+S > WSL
- Install Docker CE:
```for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
- Build image with Buildozer:
```
docker build --tag=kivy/buildozer .
```
- Build Android App
```
mkdir -p docker/{buildozer,gradle}
sudo docker run --rm -u "$(id -u):$(id -g)" -v "$(pwd)/docker/buildozer":/home/user/.buildozer -v "$(pwd)/docker/gradle":/home/user/.gradle -v "$(pwd)/app":/home/user/hostcwd kivy/buildozer -v android debug
```

## Know issues:
### Exception:</br>
```
ImportError: dlopen failed: "/data/data/org.test.app/files/app/_python_bundle/site-packages/pygame/base.so" is for EM_X86_64 (62) instead of EM_AARCH64 (183)
```
### Diagnosis:</br>
It's issue with compile pygame for ARM architecture of CPU.</br>
As alternative of Pygame module use Pygame-CE https://pypi.org/project/pygame-ce/#files</br>
Recipe for Buildozer(p4a) 
https://github.com/kivy/python-for-android/pull/2971</br> 
https://blog.emersonmx.dev/posts/difficulties-in-building-a-pygame-game-for-android/</br>
https://gist.github.com/emersonmx/c5bba202506e3c3d2d828ad278a8d5fe
### Solution:</br>
Create directory path and add recipe</br>
https://gist.githubusercontent.com/emersonmx/c5bba202506e3c3d2d828ad278a8d5fe/raw/03acfc307051438f9d0f5ef0507527920b4ee65c/pygame-ce-recipe.py
```
app\p4-recipes\pygame-ce\__init__.py
```
### Exception :</br>
```
suncompass\.buildozer\android\platform\android-ndk-r25b-linux.zip<br /> OR replace android-ndk-r25b/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include/linux/netfilter_ipv4/ipt_ecn.h? [y]es, [n]o, [A]ll, [N]one, [r]ename:  NULL (EOF or read error, treating as "[N]one"
Press [A]
```
### Solution:</br>
Unpack manually the Android NDK archive in case of issue with buildozer unarchiving

### Symptoms :</br>
```
CMake Error at /usr/share/cmake-3.22/Modules/CMakeTestCCompiler.cmake:69 (message): The C compiler<p>
```
### Resolving:</br>
delete dir
```
rm -rf .buildozer\android\platform\build-arm64-v8a_armeabi-v7a\build\other_builds\jpeg\arm64-v8a__ndk_target_21\jpeg\CMakeFiles
```
### Issue :</br>
```Execution failed for task ':packageDebug'.
> A failure occurred while executing com.android.build.gradle.tasks.PackageAndroidArtifact$IncrementalSplitterRunnable
   > java.lang.OutOfMemoryError (no error message)
```
### How to fix:</br>
Increase memory limits for JVM
```
.buildozer\android\platform\build-[arch_name]\dists\[appname]\templates\gradle.tmpl.properties```
```
Increase memory limits for WSL2 VM:</br>
```
%userprofile%\.wslconfig

[wsl2]
memory=8GB
processors=8

wsl -shutdown
```