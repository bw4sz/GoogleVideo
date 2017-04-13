# MotionMeerkat in the cloud

Observing biodiversity is expensive and time-consuming. Ecologists are increasingly turning to long duration video to locate, count and identify animals in natural environments. However, scientists currently waste hundreds of hours manually watching and annotating frames. Automated video analysis using computer vision will increase the efficiency of ecological sampling and allow scientists to understand the effect of global change on biodiversity.

I am building a cloud platform for scientists to annotate animal presence in ecological videos. My project will utilize Google’s newly announced [Cloud Video Intelligence API](https://cloud.google.com/video-intelligence/) for animal detection and massive parallelization. This will dramatically improve the reach, capability and functionality of my current desktop software for an engaged user community. 

These new tools use deep learing nueral networks to classify images contained in video sequences. 

![Butterfly](https://raw.github.com/bw4sz/GoogleVideo/dev/sample_image.jpg?)

## Installation

The following python packages need to be installed to run MotionMeerkat and the Google Cloud Video API

## File Structure

To specify a file to analyze

```
MotionMeerkat.MotionMeerkat(<pathtofile>)
```

To run general tests_basic

```
    python tests_basic.py
```

** Please note that the Google Cloud Intelligence API is current in private beta ** (4/8/2017) [Apply for access](https://cloud.google.com/video-intelligence/)
