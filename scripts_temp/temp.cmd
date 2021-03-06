@echo off

for %%m in (3) do (
for %%t in (0) do (
for %%n in (1) do (
:: for %%d in (0, 1) do (
for %%d in (1) do (
:: for %%l in (0.1, 0.5, 1) do (
for %%r in (0.0001) do (

python train_paired.py lenet_standard ^
--data_path data\\mnist.pkl ^
--paired_data_path adversarial\\fgsm\\fgsm_epsilon_0.3.pkl ^
--method %%m ^
--reg_object %%t ^
--reg_layers %%n ^
--use_dropout %%d ^
--reg %%r ^
--new_model_name fgsm_0.3_onto_std_M%%m_T%%t_N%%n_D%%d_R%%r ^
--epoch 50

python eval.py fgsm_0.3_onto_std_M%%m_T%%t_N%%n_D%%d_R%%r ^
--test_only_data_path data\\reserved.pkl ^
--method %%m ^
--reg_object %%t ^
--reg_layers %%n ^
--use_dropout %%d ^
--reg %%r ^
--use_reg_model

)))))
