import gradio as gr

def wall_follow_params_set(lookahead_dist, kp, kd, ki):
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
    
    return lookahead_dist, kp, kd, ki

demo = gr.Interface(
    wall_follow_params_set,
    inputs=[
        gr.Slider(minimum=0, maximum=10, step=0.1, label="Lookahead Distance", value=0.8),
        gr.Slider(minimum=0, maximum=10, step=0.1, label="Proportional Gain (Kp)", value=0.8),
        gr.Slider(minimum=0, maximum=10, step=0.1, label="Derivative Gain (Kd)", value=0.0),
        gr.Slider(minimum=0, maximum=5, step=0.001, label="Integral Gain (Ki)", value=0.0)
    ],
    outputs=[
        gr.Textbox(label="Lookahead Distance"),
        gr.Textbox(label="Proportional Gain (Kp)"),
        gr.Textbox(label="Derivative Gain (Kd)"),
        gr.Textbox(label="Integral Gain (Ki)")
    ],
    examples=[
        [2.0, 1.0, 0.5, 0.1],
        [3.5, 2.0, 1.0, 0.05]
    ],
    title="Wall Following Parameters Set",
    description="Set the parameters for wall following behavior in a F1/10 Car.",
    article="Use the sliders to adjust the parameters for wall following behavior. The values will be used in the PID controller for the robot's navigation.",
    flagging_mode="manual",
    flagging_dir="roboracer_flagged_data/wall_follow",
    theme="soft",
    )

demo.launch()