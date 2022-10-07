package manage conan

`https://docs.conan.io/en/latest/getting_started.html`

package files
conanfile.txt

Fresh setup

1. install dependencies

```
conan install <path_to_conanfile>

// in case of ERROR: Missing binary
conan install <path_to_conanfile> --build=missing
```

2. build with cmake

```
cmake <path_to_cmakefile> -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
cmake --build <path_to_cmakefile>
```

3. executable file is emitted to bin/ folder which can be executed

other times if you made changes to code then just run the following

```
cmake --build <path_to_cmakefile>
```

and run the executable file emitted in the bin/ directory
