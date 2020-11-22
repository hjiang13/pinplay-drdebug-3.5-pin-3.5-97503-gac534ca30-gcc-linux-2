/*
 Licensed under the BSD License:

 Copyright (c) 2012, 2013, 2014, Regents of the University of California.
 All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification,
 are permitted provided that the following conditions are met:

 -  Redistributions of source code must retain the above copyright notice,
 this
 list of conditions and the following disclaimer.
 -  Redistributions in binary form must reproduce the above copyright notice,
 this list of conditions and the following disclaimer in the documentation
 and/or other materials provided with the distribution.
 -  Neither the name of the University of California, Riverside nor the names
 of its contributors may be used to endorse or promote products derived
 from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
 DISCLAIMED.
 IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY 
 DIRECT,
 INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
 OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
 ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/*
 * @ORIGINAL_AUTHOR: Yan Wang <wangy@cs.ucr.edu>
 * @COMMENTS For queries, contact Yan Wang <wangy@cs.ucr.edu> or 
 * Rajiv Gupta <gupta@cs.ucr.edu>
 * @COMMENTS This code was developed during Yan Wang's doctoral work under the
 * supervision of Prof. Rajiv Gupta at the University of California, Riverside.
 */

/*
 * DrDebug: Deterministic Replay based Cyclic Debugging with Dynamic Slicing.
 * Please refer to our CGO'14 paper for more details:
 * Yan Wang, Harish Patil, Cristiano Pereira, Gregory Lueck, Rajiv Gupta, 
    and Iulian Neamtiu,
 * "DrDebug: Deterministic Replay based Cyclic Debugging with Dynamic Slicing",
 * IEEE/ACM International Symposium on Code Generation and Optimization 
   (CGO'14), 11 pages, Orlando, Florida, USA, February 2014
 */

#ifndef SLICE_ENGINE_H
#define SLICE_ENGINE_H

#include "pin.H"

//#define GENERATE_SEQUENCE_OF_SLICE_CRITERIA_FOR_EXPERIMENT 

class SLICE_ENGINE_IMPL;

class SLICE_ENGINE {
public:
    SLICE_ENGINE();
    VOID Activate(int argc, char *argv[], VOID *pinplay_engine);
    static SLICE_ENGINE_IMPL * Impl();

private:
    static SLICE_ENGINE_IMPL *_impl;
};

#endif
