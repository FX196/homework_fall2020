# Model Based Reinforcement Learning

## Q1
![n500_arch1x32](run_logs/hw4_q1_cheetah_n500_arch1x32_cheetah-cs285-v0_03-11-2020_04-55-56/itr_0_predictions.png)

![n5_arch2x250](run_logs/hw4_q1_cheetah_n5_arch2x250_cheetah-cs285-v0_03-11-2020_04-56-44/itr_0_predictions.png)

![n500_arch2x250](run_logs/hw4_q1_cheetah_n500_arch2x250_cheetah-cs285-v0_03-11-2020_04-57-06/itr_0_predictions.png)

The three plots shown above are from n500_arch1x32, n5_arch2x250, and n500_arch2x250 respectively. The first plot shows the the prediction was ok, staying close to the actual trajectory although deviating a little. The MPE was pretty low. The second plot performed much worse, barely fitting the trajectory. The third plot had a much lower MPE and was able to fit the trajectory almost exactly. This shows that having a larger model can help fit the dymanics model better, but training time is also a large factor. If a model is not allowed to converge, increasing the size won't do much.

## Q2

![](q2.png)

## Q3

![](q3_c.png)

![](q3_r.png)

![](q3_o.png)

## Q4

![](q4_ensemble.png)

In the above plot we show the performance of agents with different ensemble sizes. It's quite visible that the agents with higher ensemble sizes converge faster, and tend to reach higher returns. This makes sense as the agent is expected to fit the dynamics model better with a larger ensemble size.

![](q4_horizon.png)

The horizon experiment results seems counterintuitive, as one might think that planning further ahead would allow the agent to perform better. However, the model with the shortest horizon performed the best out of the three, and the one with the longest horizon performed the worst. This might be because the model isn't able to predict the future state accurately with longer horizons, so the estimated returns are bad estimates.

![](q4_numseq.png)

It makes sense that when the number of candidate action sequences increase, the model performs better, since having more candidate sequences allows the model to have a better sample of the action space.
