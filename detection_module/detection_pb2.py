# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: detection.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x64\x65tection.proto\x12\x08services\"\x1d\n\x07Request\x12\x12\n\nip_address\x18\x01 \x01(\t\"\x1a\n\x08Response\x12\x0e\n\x06status\x18\x01 \x01(\x08\x32J\n\x10\x44\x65tectionService\x12\x36\n\x0b\x43heckStatus\x12\x11.services.Request\x1a\x12.services.Response\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'detection_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUEST._serialized_start=29
  _REQUEST._serialized_end=58
  _RESPONSE._serialized_start=60
  _RESPONSE._serialized_end=86
  _DETECTIONSERVICE._serialized_start=88
  _DETECTIONSERVICE._serialized_end=162
# @@protoc_insertion_point(module_scope)
