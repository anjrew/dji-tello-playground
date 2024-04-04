# Face Tracking

To use the face tracking, we need to install additional dependencies.

If you're on Windows, you need to have installed Visual Studio with C++ build tools
see [this guide](./installing_vs_build_tools.md) on how to install them.

Then in the CLI in the face_tracking directory run
```bash
pip install -r requirements.txt
```

## Running the face tracking

First, lets do a sanity check to see if the face tracking works. Run the following command in the CLI in the face_tracking directory
```bash
python sanity_check.py
```



To run the face tracking, run the following command in the CLI in the face_tracking directory
```bash
python face_tracking.py
```