import gradio as gr
import os
import time
import json

file_dir = "roboracer_flagged_data/gap_follow"
os.makedirs(file_dir, exist_ok=True)

file_dir_ws = "../roboracer-ws/src/gap_follow_ui_control/config"
os.makedirs(file_dir_ws, exist_ok=True)

colcon_build_file_dir_ws = "../roboracer-ws/install/gap_follow_ui_control/share/gap_follow_ui_control/config"

def gap_follow_params_set(set_throttle, throttle, window_half_size, disparity_extender, max_actionable_dist):
    """
    This function sets the parameters for gap following behavior in a robot.

    Parameters:
    throttle (float): Throttle of the car.
    window_half_size (int): Minimum Consecutive values to be considered a gap.
    disparity_extender (int): Up till what values to extend disparity.
    max_actionable_dist (float): Max Distance below which the car takes some action.

    Returns:
    tuple: A tuple containing the lookahead distance, window_half_size, disparity_extender, and max_actionable_dist.
    """

    if set_throttle:
        flagged_text = (
        "{\n"
        f'\t"throttle": \t{throttle},\n'
        f'\t"window_half_size": \t{window_half_size},\n'
        f'\t"disparity_extender": \t{disparity_extender},\n'
        f'\t"max_actionable_dist": \t{max_actionable_dist},\n'
        "}"
        )
        return throttle, window_half_size, disparity_extender, max_actionable_dist, flagged_text
    else:
        flagged_text = (
        "{\n"
        f'\t"throttle": \tnull,\n'
        f'\t"window_half_size": \t{window_half_size},\n'
        f'\t"disparity_extender": \t{disparity_extender},\n'
        f'\t"max_actionable_dist": \t{max_actionable_dist},\n'
        "}"
        )
        return None, window_half_size, disparity_extender, max_actionable_dist, flagged_text

def flag_configuration(use_throttle, throttle, window_half_size, disparity_extender, max_actionable_dist, flag_reason, flag_msg):
        """
        This function flags the configuration of the gap following parameters.
        It saves the flagged data to a JSON file.
        """

        if not use_throttle:
            throttle = None
        
        flagged_data = {
            "throttle": throttle,
            "window_half_size": window_half_size,
            "disparity_extender": disparity_extender,
            "max_actionable_dist": max_actionable_dist,
            "flag_reason": flag_reason,
            "flag_msg": flag_msg
        }

        timestamp = int(time.time())
        filename = f"{file_dir}/flagged_data_{timestamp}.json"
        
        filenamelatest = f"{file_dir_ws}/gap_follow_params.json"

        filename_ws = f"{colcon_build_file_dir_ws}/gap_follow_params.json"

        try:
            # Store with timestamp
            with open(filename, "w") as f:
                json.dump(flagged_data, f, indent=4)

            # Store before colcon build
            with open(filenamelatest, "w") as f:
                json.dump(flagged_data, f, indent=4)

            # Store after colcon build
            with open(filename_ws, "w") as f:
                json.dump(flagged_data, f, indent=4)

            return f"Flagged data saved to locations: \n{filename} \n{filenamelatest} \n{filename_ws}"
        except Exception as e:
            return f"Error saving flagged data: {str(e)}"

with gr.Blocks(theme="soft", title="Set Gap Follow Parameters") as demo:
    
    gr.Markdown("## Set Gap Follow Parameters")
    gr.Markdown("Set the parameters for gap following behavior in the F1/10 Vehicle.")
    gr.Markdown("Use the sliders to adjust the parameters for gap following behavior. The values will be used in the PID controller for the robot's navigation.")
    
    with gr.Row():
        with gr.Column():
            # Throttle Control
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Throttle Control")
                    use_throttle = gr.Checkbox(label="Set Throttle", value=True)

                with gr.Column():
                    throttle = gr.Slider(minimum=-1, maximum=1, step=0.01, label="Throttle", value=0.1, interactive=True)

            # Gap Follow Parameters
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Gap Follow Parameters")
                    window_half_size = gr.Slider(minimum=0, maximum=500, step=1, label="Window Half", value=40, interactive=True)
                    disparity_extender = gr.Slider(minimum=0, maximum=500, step=1, label="Disparity Extender", value=50, interactive=True)
                    max_actionable_dist = gr.Slider(minimum=0, maximum=10, step=0.1, label="Max Actionable Distance", value=2.0, interactive=True)

                    submit_button = gr.Button("Set Parameters", variant="primary")

        with gr.Column():
            
            gr.Markdown("### Flagging")

            # Flagging

            flagged_text = gr.TextArea(label="Flagging Configuration", interactive=False)

            gr.Textbox(label="Flagging Directory", value=file_dir, interactive=False) 
            op_throttle = gr.Textbox(label="throttle", visible=False)
            op_window_half_size = gr.Textbox(label="window_half_size", visible=False)
            op_disparity_extender = gr.Textbox(label="disparity_extender", visible=False)
            op_max_actionable_dist = gr.Textbox(label="max_actionable_dist", visible=False)
            
            with gr.Row():
                flag_reason = gr.Dropdown(
                    choices=["Latest", "Golden", "Unstable Control", "Too Slow", "Too Agressive" , "Other"],
                    label="Flagging Reason",
                    value="Latest",
                    interactive=True
                )
                flag_msg = gr.Textbox(label="Flagging Message", placeholder="Optional Flagging Message.", interactive=True)

            with gr.Row():
                flag_button = gr.Button("Flag this configuration", variant="primary")

            with gr.Row():
                flag_result = gr.Textbox(label="Flagging Result")

    with gr.Row():
        # Examples
        gr.Examples(
            examples=[
                [True, 0.2, 40, 50, 2.0],
                [False, '-', 40, 50, 3.0],
                [True, 0.3, 50, 60, 3.0]
            ],
            inputs=[use_throttle, throttle, window_half_size, disparity_extender, max_actionable_dist],
            outputs=[throttle, window_half_size, disparity_extender, max_actionable_dist],
        )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("")
            gr.Markdown("")    
            gr.Markdown("")

            gr.Markdown(
                """
                ## Instructions
                
                1. Use the sliders to adjust the parameters to affect the Gap Following Behaviour.
                2. Check "Set Throttle" if you want to set throttle manually (As oposed to throttle being set on the steering angle).
                3. Click "Set parameters" to see the current configuration before flagging.
                4. Once you are ready, click on "Flag this configuration" to save the configuration in a JSON file (Read inside ros2 gap_follow node).
                
                All flagged configurations will be saved with timestamps.
                """
            )

    def activate_throttle(set_throttle):
        return gr.Slider(visible=set_throttle)            

    use_throttle.change(
        fn=activate_throttle, 
        inputs=use_throttle, 
        outputs=throttle
        )
    
    submit_button.click(
        fn = gap_follow_params_set,
        inputs=[use_throttle, throttle, window_half_size, disparity_extender, max_actionable_dist],
        outputs=[op_throttle, op_window_half_size, op_disparity_extender, op_max_actionable_dist, flagged_text]
    )
    
    flag_button.click(
        fn=flag_configuration,
        inputs=[use_throttle, op_throttle, op_window_half_size, op_disparity_extender, op_max_actionable_dist, flag_reason, flag_msg],
        outputs=flag_result
    )

demo.launch()