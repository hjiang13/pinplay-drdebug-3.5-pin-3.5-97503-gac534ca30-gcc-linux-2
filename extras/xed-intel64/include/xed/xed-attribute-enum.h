/*BEGIN_LEGAL 
Intel Open Source License 

Copyright (c) 2002-2017 Intel Corporation. All rights reserved.
 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.  Redistributions
in binary form must reproduce the above copyright notice, this list of
conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.  Neither the name of
the Intel Corporation nor the names of its contributors may be used to
endorse or promote products derived from this software without
specific prior written permission.
 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE INTEL OR
ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
END_LEGAL */
/// @file xed-attribute-enum.h

// This file was automatically generated.
// Do not edit this file.

#if !defined(XED_ATTRIBUTE_ENUM_H)
# define XED_ATTRIBUTE_ENUM_H
#include "xed-common-hdrs.h"
typedef enum {
  XED_ATTRIBUTE_INVALID,
  XED_ATTRIBUTE_ATT_OPERAND_ORDER_EXCEPTION,
  XED_ATTRIBUTE_BROADCAST_ENABLED,
  XED_ATTRIBUTE_BYTEOP,
  XED_ATTRIBUTE_DISP8_EIGHTHMEM,
  XED_ATTRIBUTE_DISP8_FULL,
  XED_ATTRIBUTE_DISP8_FULLMEM,
  XED_ATTRIBUTE_DISP8_GPR_READER,
  XED_ATTRIBUTE_DISP8_GPR_READER_BYTE,
  XED_ATTRIBUTE_DISP8_GPR_READER_WORD,
  XED_ATTRIBUTE_DISP8_GPR_WRITER_LDOP_D,
  XED_ATTRIBUTE_DISP8_GPR_WRITER_LDOP_Q,
  XED_ATTRIBUTE_DISP8_GPR_WRITER_STORE,
  XED_ATTRIBUTE_DISP8_GPR_WRITER_STORE_BYTE,
  XED_ATTRIBUTE_DISP8_GPR_WRITER_STORE_WORD,
  XED_ATTRIBUTE_DISP8_GSCAT,
  XED_ATTRIBUTE_DISP8_HALF,
  XED_ATTRIBUTE_DISP8_HALFMEM,
  XED_ATTRIBUTE_DISP8_MEM128,
  XED_ATTRIBUTE_DISP8_MOVDDUP,
  XED_ATTRIBUTE_DISP8_QUARTERMEM,
  XED_ATTRIBUTE_DISP8_SCALAR,
  XED_ATTRIBUTE_DISP8_TUPLE1,
  XED_ATTRIBUTE_DISP8_TUPLE1_4X,
  XED_ATTRIBUTE_DISP8_TUPLE1_BYTE,
  XED_ATTRIBUTE_DISP8_TUPLE1_WORD,
  XED_ATTRIBUTE_DISP8_TUPLE2,
  XED_ATTRIBUTE_DISP8_TUPLE4,
  XED_ATTRIBUTE_DISP8_TUPLE8,
  XED_ATTRIBUTE_DOUBLE_WIDE_MEMOP,
  XED_ATTRIBUTE_DOUBLE_WIDE_OUTPUT,
  XED_ATTRIBUTE_DWORD_INDICES,
  XED_ATTRIBUTE_ELEMENT_SIZE_D,
  XED_ATTRIBUTE_ELEMENT_SIZE_Q,
  XED_ATTRIBUTE_EXCEPTION_BR,
  XED_ATTRIBUTE_FAR_XFER,
  XED_ATTRIBUTE_FIXED_BASE0,
  XED_ATTRIBUTE_FIXED_BASE1,
  XED_ATTRIBUTE_GATHER,
  XED_ATTRIBUTE_HALF_WIDE_OUTPUT,
  XED_ATTRIBUTE_HLE_ACQ_ABLE,
  XED_ATTRIBUTE_HLE_REL_ABLE,
  XED_ATTRIBUTE_IGNORES_OSFXSR,
  XED_ATTRIBUTE_IMPLICIT_ONE,
  XED_ATTRIBUTE_INDEX_REG_IS_POINTER,
  XED_ATTRIBUTE_INDIRECT_BRANCH,
  XED_ATTRIBUTE_KMASK,
  XED_ATTRIBUTE_LOCKABLE,
  XED_ATTRIBUTE_LOCKED,
  XED_ATTRIBUTE_MASKOP,
  XED_ATTRIBUTE_MASKOP_EVEX,
  XED_ATTRIBUTE_MASK_AS_CONTROL,
  XED_ATTRIBUTE_MASK_VARIABLE_MEMOP,
  XED_ATTRIBUTE_MEMORY_FAULT_SUPPRESSION,
  XED_ATTRIBUTE_MMX_EXCEPT,
  XED_ATTRIBUTE_MPX_PREFIX_ABLE,
  XED_ATTRIBUTE_MULTISOURCE4,
  XED_ATTRIBUTE_MXCSR,
  XED_ATTRIBUTE_MXCSR_RD,
  XED_ATTRIBUTE_NONTEMPORAL,
  XED_ATTRIBUTE_NOP,
  XED_ATTRIBUTE_NOTSX,
  XED_ATTRIBUTE_NOTSX_COND,
  XED_ATTRIBUTE_NO_RIP_REL,
  XED_ATTRIBUTE_PREFETCH,
  XED_ATTRIBUTE_PROTECTED_MODE,
  XED_ATTRIBUTE_QWORD_INDICES,
  XED_ATTRIBUTE_REP,
  XED_ATTRIBUTE_REQUIRES_ALIGNMENT,
  XED_ATTRIBUTE_RING0,
  XED_ATTRIBUTE_SCALABLE,
  XED_ATTRIBUTE_SCATTER,
  XED_ATTRIBUTE_SIMD_SCALAR,
  XED_ATTRIBUTE_SKIPLOW32,
  XED_ATTRIBUTE_SKIPLOW64,
  XED_ATTRIBUTE_SPECIAL_AGEN_REQUIRED,
  XED_ATTRIBUTE_STACKPOP0,
  XED_ATTRIBUTE_STACKPOP1,
  XED_ATTRIBUTE_STACKPUSH0,
  XED_ATTRIBUTE_STACKPUSH1,
  XED_ATTRIBUTE_X87_CONTROL,
  XED_ATTRIBUTE_X87_MMX_STATE_CW,
  XED_ATTRIBUTE_X87_MMX_STATE_R,
  XED_ATTRIBUTE_X87_MMX_STATE_W,
  XED_ATTRIBUTE_X87_NOWAIT,
  XED_ATTRIBUTE_XMM_STATE_CW,
  XED_ATTRIBUTE_XMM_STATE_R,
  XED_ATTRIBUTE_XMM_STATE_W,
  XED_ATTRIBUTE_LAST
} xed_attribute_enum_t;

/// This converts strings to #xed_attribute_enum_t types.
/// @param s A C-string.
/// @return #xed_attribute_enum_t
/// @ingroup ENUM
XED_DLL_EXPORT xed_attribute_enum_t str2xed_attribute_enum_t(const char* s);
/// This converts strings to #xed_attribute_enum_t types.
/// @param p An enumeration element of type xed_attribute_enum_t.
/// @return string
/// @ingroup ENUM
XED_DLL_EXPORT const char* xed_attribute_enum_t2str(const xed_attribute_enum_t p);

/// Returns the last element of the enumeration
/// @return xed_attribute_enum_t The last element of the enumeration.
/// @ingroup ENUM
XED_DLL_EXPORT xed_attribute_enum_t xed_attribute_enum_t_last(void);
#endif
