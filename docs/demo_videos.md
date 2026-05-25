# Demo Videos

These videos show the SDK demos running on the real robot.

## GitHub Playback

GitHub does not reliably render repository-relative MP4 files from an HTML
`<video>` tag in Markdown. To show an inline player on GitHub:

1. Open an issue, pull request, or discussion comment on GitHub.
2. Drag the `.mp4` file into the comment box and wait for GitHub to upload it.
3. Copy the generated `https://github.com/user-attachments/assets/...` URL.
4. Paste that URL on its own line in the "GitHub player URL" slot below.

GitHub upload limits are 10 MB for videos on free user/organization repositories
and 100 MB on paid plans. `demo1.mp4` is currently larger than 10 MB, so compress
it before uploading on a free plan.

## Demo 1: Performance Routine

- Script: [`demo/demo_1_performance.py`](../demo/demo_1_performance.py)
- Local MP4: [`docs/assets/demos/demo1.mp4`](assets/demos/demo1.mp4)
- Shows: ears, expressions, actions, forward movement, angle turning, slow crouch, sleepy expression, stretch, and tail wag.

Performance sequence:

1. Connect to the robot and disable special detection.
2. Raise the ears and show a yawn expression.
3. Shake hand three times.
4. Nod twice.
5. Move forward for 2 seconds while playing `BEAT1`.
6. Jump.
7. Turn right by angle command.
8. Enter a long slow crouch and switch to a sleepy expression.
9. Stretch.
10. Wag tail three times, stop audio, reset, and re-enable special detection.

GitHub player URL: https://github.com/user-attachments/assets/dc8c8bea-d5ef-4b3a-bc0b-4af86d036a9c

<!-- Paste the GitHub-uploaded video URL on the next line. It must be a bare URL, not a Markdown link. -->

## Demo 2: Custom Action

- Script: [`demo/demo_2_custom_action.py`](../demo/demo_2_custom_action.py)
- Local MP4: [`docs/assets/demos/demo2.mp4`](assets/demos/demo2.mp4)
- Shows: forward movement followed by a custom sniff-like action built from smooth body/foot adjustment, expression, and audio.

Performance sequence:

1. Connect to the robot.
2. Move forward for 1.5 seconds.
3. Show a happy expression and stop movement.
4. Disable special detection and TOF avoidance for custom adjustment.
5. Request basic mode and move to a baseline pose.
6. Shift all four feet backward to prepare the body.
7. Lift both front legs and pull them back slightly.
8. Play the eating tone and show the eat-snack expression twice.
9. Restore the front-leg lift and X adjustment.
10. Restore the full-body foot shift.
11. Request basic mode, restore TOF avoidance, re-enable special detection, and reset.

GitHub player URL: https://github.com/user-attachments/assets/7a0e693a-2233-4a02-b598-6bd877eeb91f

<!-- Paste the GitHub-uploaded video URL on the next line. It must be a bare URL, not a Markdown link. -->

## Demo 3: Reactive Companion Patrol

- Script: [`demo/demo_3_reactive_companion.py`](../demo/demo_3_reactive_companion.py)
- Local MP4: not recorded yet.
- Shows: stretch wake-up, TOF-based patrol, obstacle detection, short retreat, and whining/tantrum reaction.

Performance sequence:

1. Connect to the robot.
2. Disable special detection and enable TOF avoidance.
3. Raise the ears and play the wake-up tone.
4. Perform a stretch action.
5. Stop audio and show a happy expression.
6. Start the TOF stream and warm up sensor notifications.
7. Patrol forward in short pulses while reading `front_mm`.
8. If a close obstacle is detected, stop movement immediately.
9. Show a doubt expression, flick the ears, and play the doubt tone.
10. Move backward briefly.
11. Switch to a sad expression, lower the ears, and play the sad tone.
12. Perform the `WHINING` action as the tantrum reaction.
13. Stop audio, restore standing ears, turn off the TOF stream, re-enable special detection, and reset.

GitHub player URL: https://github.com/user-attachments/assets/2617ad17-811a-44ad-8f8e-68e7ccb64f2c

<!-- Paste the GitHub-uploaded video URL on the next line. It must be a bare URL, not a Markdown link. -->

## Notes

- Run the demos in an open area and keep the robot away from table edges or stairs.
- Use a charged battery before recording or demonstrating long action sequences.
- The local MP4 links are still useful for cloning the repository and opening the
  files directly.
