import gradio as gr
import os
import time
import json

file_dir = "roboracer_flagged_data/wall_follow"
os.makedirs(file_dir, exist_ok=True)

def wall_follow_params_set(set_throttle, throttle, lookahead_dist, kp, kd, ki):
    """
    This function sets the parameters for wall following behavior in a robot.

    Parameters:
    lookahead_dist (float): The distance to look ahead for wall following.
    kp (float): Proportional gain for the PID controller.
    kd (float): Derivative gain for the PID controller.
    ki (float): Integral gain for the PID controller.

    Returns:
    tuple: A tuple containing the lookahead distance, proportional gain, derivative gain, and integral gain.
    """

    if set_throttle:
        flagged_text = (
        "{\n"
        f'\t"Throttle": \t{throttle},\n'
        f'\t"Lookahead Distance": \t{lookahead_dist},\n'
        f'\t"Kp": \t{kp},\n'
        f'\t"Kd": \t{kd},\n'
        f'\t"Ki": \t{ki}\n'
        "}"
        )
        return throttle, lookahead_dist, kp, kd, ki, flagged_text
    else:
        flagged_text = (
        "{\n"
        f'\t"Throttle": \tnull,\n'
        f'\t"Lookahead Distance": \t{lookahead_dist},\n'
        f'\t"Kp": \t{kp},\n'
        f'\t"Kd": \t{kd},\n'
        f'\t"Ki": \t{ki}\n'
        "}"
        )
        return None, lookahead_dist, kp, kd, ki, flagged_text

def flag_configuration(use_throttle, throttle, lookahead_dist, kp, kd, ki, flag_reason, flag_msg):
        """
        This function flags the configuration of the wall following parameters.
        It saves the flagged data to a JSON file.
        """

        if not use_throttle:
            throttle = None
        
        flagged_data = {
            "throttle": throttle,
            "lookahead_dist": lookahead_dist,
            "kp": kp,
            "kd": kd,
            "ki": ki,
            "flag_reason": flag_reason,
            "flag_msg": flag_msg
        }

        timestamp = int(time.time())
        filename = f"{file_dir}/flagged_data_{timestamp}.json"

        try:
            with open(filename, "w") as f:
                json.dump(flagged_data, f, indent=4)

            return f"Flagged data saved to {filename}."
        except Exception as e:
            return f"Error saving flagged data: {str(e)}"

with gr.Blocks(theme="soft", title="Set Wall Follow Parameters") as demo:
    
    gr.Markdown("## Set Wall Follow Parameters")
    gr.Markdown("Set the parameters for wall following behavior in the F1/10 Vehicle.")
    gr.Markdown("Use the sliders to adjust the parameters for wall following behavior. The values will be used in the PID controller for the robot's navigation.")
    
    with gr.Row():
        with gr.Column():
            # Throttle Control
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Throttle Control")
                    use_throttle = gr.Checkbox(label="Set Throttle", value=True)

                with gr.Column():
                    throttle = gr.Slider(minimum=-1, maximum=1, step=0.01, label="Throttle", value=0.1, interactive=True)

            # Wall Follow Parameters
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Wall Follow Parameters")
                    lookahead_dist = gr.Slider(minimum=0, maximum=10, step=0.1, label="Lookahead Distance", value=0.8, interactive=True)
                    kp = gr.Slider(minimum=0, maximum=10, step=0.1, label="Proportional Gain (Kp)", value=0.8, interactive=True)
                    kd = gr.Slider(minimum=0, maximum=10, step=0.1, label="Derivative Gain (Kd)", value=0.0, interactive=True)
                    ki = gr.Slider(minimum=0, maximum=5, step=0.001, label="Integral Gain (Ki)", value=0.0, interactive=True)

                    submit_button = gr.Button("Set Parameters", variant="primary")

        with gr.Column():
            
            gr.Markdown("### Flagging")

            # Flagging

            flagged_text = gr.TextArea(label="Flagging Configuration", interactive=False)

            gr.Textbox(label="Flagging Directory", value=file_dir, interactive=False) 
            op_throttle = gr.Textbox(label="throttle", visible=False)
            op_lookahead_dist = gr.Textbox(label="lookahead_dist", visible=False)
            op_kp = gr.Textbox(label="kp", visible=False)
            op_kd = gr.Textbox(label="kd", visible=False)
            op_ki = gr.Textbox(label="ki", visible=False)
            
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
                [True, 0.1, 2.0, 1.0, 0.5, 0.1],
                [False, None, 3.5, 2.0, 1.0, 0.05]
            ],
            inputs=[use_throttle, throttle, lookahead_dist, kp, kd, ki],
            outputs=[throttle, lookahead_dist, kp, kd, ki],
        )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("")
            gr.Markdown("")    
            gr.Markdown("")

            gr.Markdown(
                """
                ## Instructions
                
                1. Use the sliders to adjust the parameters to affect the Wall Following Behaviour.
                2. Check "Set Throttle" if you want to set throttle manually (As oposed to throttle being set on the steering angle).
                3. Click "Set parameters" to see the current configuration before flagging.
                4. Once you are ready, click on "Flag this configuration" to save the configuration in a JSON file (Read inside ros2 wall_follow node).
                
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
        fn = wall_follow_params_set,
        inputs=[use_throttle, throttle, lookahead_dist, kp, kd, ki],
        outputs=[op_throttle, op_lookahead_dist, op_kp, op_kd, op_ki, flagged_text]
    )
    
    flag_button.click(
        fn=flag_configuration,
        inputs=[use_throttle, op_throttle, op_lookahead_dist, op_kp, op_kd, op_ki, flag_reason, flag_msg],
        outputs=flag_result
    )

demo.launch()