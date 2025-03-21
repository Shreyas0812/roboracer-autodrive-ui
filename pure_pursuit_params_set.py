import gradio as gr
import os
import time
import json

file_dir = "roboracer_flagged_data/pure_pursuit"
os.makedirs(file_dir, exist_ok=True)

file_dir_ws = "../roboracer-ws/src/pure_pursuit/config"
os.makedirs(file_dir_ws, exist_ok=True)

colcon_build_file_dir_ws = "../roboracer-ws/install/pure_pursuit/share/pure_pursuit/config"


def pure_pursuit_params_set(throttle, kp, lookahead_distance):

    flagged_text = (
        "{\n"
        f'\t"throttle": \t{throttle},\n'
        f'\t"kp": \t{kp},\n'
        f'\t"lookahead_distance": \t{lookahead_distance},\n'
        "}"
    )

    return throttle, kp, lookahead_distance, flagged_text

def flag_configuration(throttle, kp, lookahead_distance, flag_reason, flag_msg):
    """
    This function flags the configuration of the pure pursuit parameters.
    It saves the flagged data to a JSON file.
    """

    flagged_data = {
        "throttle": throttle,
        "kp": kp,
        "lookahead_distance": lookahead_distance,
        "flag_reason": flag_reason,
        "flag_msg": flag_msg
    }

    timestamp = int(time.time())
    filename = f"{file_dir}/flagged_data_{timestamp}.json"

    filenamelatest = f"{file_dir_ws}/pure_pursuit_params.json"

    filename_ws = f"{colcon_build_file_dir_ws}/pure_pursuit_params.json"

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

with gr.Blocks(theme="soft", title="Set Pure Pursuit Parameters") as demo:
    
    gr.Markdown("## Set Pure Pursuit Parameters")
    gr.Markdown("Set the parameters for pure pursuit behavior in the F1/10 Vehicle.")
    gr.Markdown("Use the sliders to adjust the parameters for pure pursuit. The values will be used in for the robot's navigation.")
    
    with gr.Row():
        with gr.Column():
            # pURE pURSUIT Parameters
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### pURE pURSUIT Parameters")
                    throttle = gr.Slider(minimum=-1, maximum=1, step=0.01, label="Target Throttle", value=0.15, interactive=True)
                    kp = gr.Slider(minimum=0, maximum=5, step=0.1, label="kp for Curvature", value=1, interactive=True)
                    lookahead_distance = gr.Slider(minimum=0, maximum=10, step=0.1, label="Lookahead Distance", value=1.2, interactive=True)

                    submit_button = gr.Button("Set Parameters", variant="primary")

        with gr.Column():
            
            gr.Markdown("### Flagging")

            # Flagging

            flagged_text = gr.TextArea(label="Flagging Configuration", interactive=False)

            gr.Textbox(label="Flagging Directory", value=file_dir, interactive=False) 
            op_throttle = gr.Textbox(label="throttle", visible=False)
            op_kp = gr.Textbox(label="kp", visible=False)
            op_lookahead_distance = gr.Textbox(label="lookahead_distance", visible=False)
            
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
                [0.15, 1, 1.2],
            ],
            inputs=[throttle, kp, lookahead_distance],
            outputs=[throttle, kp, lookahead_distance],
        )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("")
            gr.Markdown("")    
            gr.Markdown("")

            gr.Markdown(
                """
                ## Instructions
                
                1. Use the sliders to adjust the parameters to affect the Pure Pursuit Behaviour.
                2. Click "Set parameters" to see the current configuration before flagging.
                3. Once you are ready, click on "Flag this configuration" to save the configuration in a JSON file (Read inside ros2 pure_pursuit node).
                
                All flagged configurations will be saved with timestamps.
                """
            )

    def activate_throttle(set_throttle):
        return gr.Slider(visible=set_throttle)            
    
    submit_button.click(
        fn = pure_pursuit_params_set,
        inputs=[throttle, kp, lookahead_distance],
        outputs=[op_throttle, op_kp, op_lookahead_distance, flagged_text]
    )
    
    flag_button.click(
        fn=flag_configuration,
        inputs=[op_throttle, op_kp, op_lookahead_distance, flag_reason, flag_msg],
        outputs=flag_result
    )

demo.launch()