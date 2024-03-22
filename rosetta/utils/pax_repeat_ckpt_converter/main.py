# Copyright (c) 2023, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse

from paxml_converters import NonRepeat2RepeatConvertHelper
from utils import ModelConfig

PAX = 'pax'

def parse_args():
    parser = argparse.ArgumentParser(description="Pax Non-repeat to repeat CKPT Converter.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--input-path',
                        type=str,
                        required=True,
                        help="the path to load a source checkponint for this conversion.")
    parser.add_argument('--output-path',
                        type=str,
                        required=True,
                        help="the path to store the converted checkponint.")
    parser.add_argument('--num-of-layer',
                        type=int,
                        required=True,
                        help="the number of Transformer layer of the given source checkpoint.")
    parser.add_argument(
        '--num-of-head',
        type=int,
        required=True,
        help="the number of head of multi-head attention of the given source checkpoint.")
    parser.add_argument(
        '--head-dim',
        type=int,
        required=True,
        help="the head dimension of multi-head attention of the given source checkpoint.")
    parser.add_argument(
        '--mlp-intermediate-dim',
        type=int,
        required=True,
        help="the intermediate dimension of MLP block (FFN) of the given source checkpoint.")
    parser.add_argument('--weight-only',
                        action="store_true",
                        default=False,
                        help="indicate if the source checkpoint only includes weights.")
    parser.add_argument('--skip-bias',
                        action="store_true",
                        default=False,
                        help="indicate whether the source checkpoint has biases.")
    args = parser.parse_args()

    return args


def get_convert_helper(args):

    model_config = ModelConfig(args.num_of_layer, args.embed_dim, args.num_of_head, args.head_dim,
                               args.mlp_intermediate_dim)

    convert_helper_cls = None

    assert convert_helper_cls is not None, "Not Supported."
    return NonRepeat2RepeatConvertHelper(args.input_path, args.output_path, model_config,
                              args.weight_only, args.skip_bias)


if __name__ == "__main__":
    args = parse_args()
    convert_helper = get_convert_helper(args)
    convert_helper.convert()
