from argparse import ArgumentParser
from methods.hypernets.hypernet_poc import ALLOWED_AGGREGATIONS


def add_hn_args_to_parser(parser: ArgumentParser) -> ArgumentParser:

    hypershot_args = parser.add_argument_group("HyperShot-related arguments")
    hypershot_args.add_argument('--hn_adaptation_strategy', type=str, default=None, choices=['increasing_alpha'], help='strategy used for manipulating alpha parameter')
    hypershot_args.add_argument('--hn_alpha_step', type=float, default=0, help='step used to increase alpha from 0 to 1 during adaptation to new task')
    hypershot_args.add_argument("--hn_hidden_size", type=int, default=256, help="HN hidden size")
    hypershot_args.add_argument("--hn_tn_hidden_size", type=int, default=120, help="TN hidden size")
    hypershot_args.add_argument("--hn_taskset_size", type=int, default=1, help="Taskset size")
    hypershot_args.add_argument("--hn_neck_len", type=int, default=0, help="Number of layers in the neck of the hypernet")
    hypershot_args.add_argument("--hn_head_len", type=int, default=2, help="Number of layers in the heads of the hypernet, must be >= 1")
    hypershot_args.add_argument("--hn_taskset_repeats", type=str, default="10:10-20:5-30:2", help="A sequence of <epoch:taskset_repeats_until_the_epoch>")
    hypershot_args.add_argument("--hn_taskset_print_every", type=int, default=20, help="It's a utility")
    hypershot_args.add_argument("--hn_detach_ft_in_hn", type=int, default=10000, help="Detach FE output before hypernetwork in training *after* this epoch")
    hypershot_args.add_argument("--hn_detach_ft_in_tn", type=int, default=10000, help="Detach FE output before target network in training *after* this epoch")
    hypershot_args.add_argument("--hn_tn_depth", type=int, default=1, help="Depth of target network")
    hypershot_args.add_argument("--hn_dropout", type=float, default=0, help="Dropout probability in hypernet")
    hypershot_args.add_argument("--hn_sup_aggregation", type=str, default="concat", choices=ALLOWED_AGGREGATIONS, help="How to aggregate supports from the same class")


    hypershot_args.add_argument("--hn_transformer_layers_no", type=int, default=1, help="Number of layers in transformer")
    hypershot_args.add_argument("--hn_transformer_heads_no", type=int, default=1, help="Number of attention heads in transformer")
    hypershot_args.add_argument("--hn_transformer_feedforward_dim", type=int, default=512, help="Transformer's feedforward dimensionality")
    hypershot_args.add_argument("--hn_attention_embedding", action='store_true', help="Utilize attention-based embedding")

    hypershot_args.add_argument("--hn_kernel_layers_no", type=int, default=2, help="Depth of a kernel network")
    hypershot_args.add_argument("--hn_kernel_hidden_dim", type=int, default=128, help="Hidden dimension of a kernel network")

    hypershot_args.add_argument("--kernel_transformer_layers_no", type=int, default=1, help="Number of layers in kernel's transformer")
    hypershot_args.add_argument("--kernel_transformer_heads_no", type=int, default=1, help="Number of attention heads in kernel's transformer")
    hypershot_args.add_argument("--kernel_transformer_feedforward_dim", type=int, default=512, help="Kernel transformer's feedforward dimensionality")
    hypershot_args.add_argument("--hn_kernel_out_size", type=int, default=1600, help="Kernel output dim")
    hypershot_args.add_argument("--hn_kernel_invariance", action='store_true', help="Should the HyperNet's kernel be sequence invariant")
    hypershot_args.add_argument("--hn_kernel_invariance_type", default='attention',  choices=['attention', 'convolution'], help="The type of invariance operation for the kernel's output")
    hypershot_args.add_argument("--hn_kernel_convolution_output_dim", type=int, default=256, help="Kernel convolution's output dim")
    hypershot_args.add_argument("--hn_kernel_invariance_pooling", default='mean',  choices=['average', 'mean', 'min', 'max'], help="The type of invariance operation for the kernel's output")

    hypershot_args.add_argument("--hn_use_support_embeddings", action='store_true', help="Concatenate support embeddings with kernel features")
    hypershot_args.add_argument("--hn_no_self_relations", action='store_true', help="Multiply matrix K to remove self relations (i.e., kernel(x_i, x_i))")
    hypershot_args.add_argument("--hn_use_cosine_distance", action='store_true', help="Use cosine distance instead of a more specific kernel")
    hypershot_args.add_argument("--hn_use_scalar_product", action='store_true', help="Use scalar product instead of a more specific kernel")
    hypershot_args.add_argument("--hn_use_cosine_nn_kernel", action='store_true', help="Use cosine distance in NNKernel")

    hypershot_args.add_argument("--hn_val_epochs", type=int, default=0, help="Epochs for finetuning on support set during validation. We recommend to set this to >0 only during testing.")
    hypershot_args.add_argument("--hn_val_lr", type=float, default=1e-4, help="LR for finetuning on support set during validation")
    hypershot_args.add_argument("--hn_val_optim", type=str, default="adam", choices=["adam", "sgd"], help="Optimizer for finetuning on support set during validation")

    #######################################
    #######################################
    # START OF BAYESIAN HYPERSHOT ARGUMENTS
    #######################################
    #######################################

    hypershot_args.add_argument('--hn_bayesian_test', action='store_true', help='Draw from random var on interference stage')

    #Without this flag model is bayesian from the beginning
    hypershot_args.add_argument('--hn_warmup', action='store_true', help="Turns on warmup between HyperShot and BayesianHyperShot")
    hypershot_args.add_argument("--hn_warmup_start_epoch", type=int, default=10, help="Start warmup at given epoch")
    hypershot_args.add_argument("--hn_warmup_stop_epoch", type=int, default=50, help="Stop warmup at given epoch")

    # describes number of forwards in target networtk for one input sample (later results are averaged)
    hypershot_args.add_argument("--hn_S", type=int, default=5, help="Number of samples.")
    hypershot_args.add_argument("--hn_S_test", type=int, default=1, help="Number of samples on test.")

    # arguments for kld constant scaling and dynamic scaling
    hypershot_args.add_argument('--hn_kld_const_scaler', default=0, type=int, help='Example: for value=-3 scaling equals 10e-3')

    hypershot_args.add_argument('--hn_use_kld_scheduler', action='store_true', help="Only with this flag we can use remaining two. Otherwise scaling is constant")
    hypershot_args.add_argument('--hn_kld_stop_val', default=-3, type=int, help='final value of kld_scale')
    hypershot_args.add_argument('--hn_kld_start_val', default=-24, type=int, help='initial value of kld_scale')

    hypershot_args.add_argument('--hn_use_kld_from', default=0, type=int, help='Include kld from epoch passed with parameter')

    # Bayesian Hyper Shot or non bayesian Hyper Shot
    hypershot_args.add_argument('--hn_bayesian_model', action='store_true', help='Uses reparametrization with this flag. Otherwise behaves like non bayesian Hyper Shot')
    hypershot_args.add_argument('--hn_use_kld', action='store_true', help="Includes KLD in cost function")
    hypershot_args.add_argument("--hn_use_mu_in_kld", action='store_true', help="Include mu in kld cost")

    #####################################
    #####################################
    # END OF BAYESIAN HYPERSHOT ARGUMENTS
    #####################################
    #####################################

    hypermaml_args =  parser.add_argument_group("HyperMAML-related arguments")

    hypermaml_args.add_argument('--hm_use_class_batch_input', action='store_true', help='Strategy for handling query set embeddings as an input of hyper network')
    hypermaml_args.add_argument("--hm_enhance_embeddings", type=bool, default=False, help="Flag that indicates if embeddings should be concatenated with logits and labels")
    hypermaml_args.add_argument("--hm_update_operator", type=str, default='minus', choices=['minus', 'plus', 'multiply'], help="Add BatchNorm to hypernet")
    hypermaml_args.add_argument('--hm_lambda', type=float, default=0.0, help='Regularization coefficient for the output of the hypernet')
    hypermaml_args.add_argument('--hm_save_delta_params', type=bool, default=False, help='saving delta parameters')

    hypermaml_args.add_argument("--hm_maml_warmup", action="store_true", help="Train the model in MAML way only at the beggining of the training")
    hypermaml_args.add_argument("--hm_maml_update_feature_net", action="store_true", help="Train feature net in the inner loop of MAML")
    hypermaml_args.add_argument("--hm_maml_warmup_epochs", type=int, default=100, help="The first n epochs where model is trained in MAML way only")
    hypermaml_args.add_argument("--hm_maml_warmup_switch_epochs", type=int, default=1000, help="The number of epochs for switching from MAML to HyperMAML")
    hypermaml_args.add_argument("--hm_load_feature_net", action="store_true", help="Load feature network from file")
    hypermaml_args.add_argument("--hm_feature_net_path", type=str, default='', help="File with feature network")
    hypermaml_args.add_argument("--hm_detach_feature_net", action="store_true", help="Freeze feature network")
    hypermaml_args.add_argument("--hm_detach_before_hyper_net", action="store_true", help="Do not calculate gradient which comes from hypernetwork")
    hypermaml_args.add_argument("--hm_support_set_loss", action='store_true', help="Use both query and support data when calculating loss")
    hypermaml_args.add_argument("--hm_set_forward_with_adaptation", action='store_true', help="Adapt network before test")
    return parser
