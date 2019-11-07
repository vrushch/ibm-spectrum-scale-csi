// +build !ignore_autogenerated

// Code generated by operator-sdk. DO NOT EDIT.

package v1alpha1

import (
	runtime "k8s.io/apimachinery/pkg/runtime"
)

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *CSIClusterSpec) DeepCopyInto(out *CSIClusterSpec) {
	*out = *in
	out.Primary = in.Primary
	if in.RestApi != nil {
		in, out := &in.RestApi, &out.RestApi
		*out = make([]CSIRestApiSpec, len(*in))
		copy(*out, *in)
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new CSIClusterSpec.
func (in *CSIClusterSpec) DeepCopy() *CSIClusterSpec {
	if in == nil {
		return nil
	}
	out := new(CSIClusterSpec)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *CSIPrimarySpec) DeepCopyInto(out *CSIPrimarySpec) {
	*out = *in
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new CSIPrimarySpec.
func (in *CSIPrimarySpec) DeepCopy() *CSIPrimarySpec {
	if in == nil {
		return nil
	}
	out := new(CSIPrimarySpec)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *CSIRestApiSpec) DeepCopyInto(out *CSIRestApiSpec) {
	*out = *in
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new CSIRestApiSpec.
func (in *CSIRestApiSpec) DeepCopy() *CSIRestApiSpec {
	if in == nil {
		return nil
	}
	out := new(CSIRestApiSpec)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *CSIScaleOperator) DeepCopyInto(out *CSIScaleOperator) {
	*out = *in
	out.TypeMeta = in.TypeMeta
	in.ObjectMeta.DeepCopyInto(&out.ObjectMeta)
	in.Spec.DeepCopyInto(&out.Spec)
	in.Status.DeepCopyInto(&out.Status)
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new CSIScaleOperator.
func (in *CSIScaleOperator) DeepCopy() *CSIScaleOperator {
	if in == nil {
		return nil
	}
	out := new(CSIScaleOperator)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyObject is an autogenerated deepcopy function, copying the receiver, creating a new runtime.Object.
func (in *CSIScaleOperator) DeepCopyObject() runtime.Object {
	if c := in.DeepCopy(); c != nil {
		return c
	}
	return nil
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *CSIScaleOperatorCondition) DeepCopyInto(out *CSIScaleOperatorCondition) {
	*out = *in
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new CSIScaleOperatorCondition.
func (in *CSIScaleOperatorCondition) DeepCopy() *CSIScaleOperatorCondition {
	if in == nil {
		return nil
	}
	out := new(CSIScaleOperatorCondition)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *CSIScaleOperatorList) DeepCopyInto(out *CSIScaleOperatorList) {
	*out = *in
	out.TypeMeta = in.TypeMeta
	out.ListMeta = in.ListMeta
	if in.Items != nil {
		in, out := &in.Items, &out.Items
		*out = make([]CSIScaleOperator, len(*in))
		for i := range *in {
			(*in)[i].DeepCopyInto(&(*out)[i])
		}
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new CSIScaleOperatorList.
func (in *CSIScaleOperatorList) DeepCopy() *CSIScaleOperatorList {
	if in == nil {
		return nil
	}
	out := new(CSIScaleOperatorList)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyObject is an autogenerated deepcopy function, copying the receiver, creating a new runtime.Object.
func (in *CSIScaleOperatorList) DeepCopyObject() runtime.Object {
	if c := in.DeepCopy(); c != nil {
		return c
	}
	return nil
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *CSIScaleOperatorSpec) DeepCopyInto(out *CSIScaleOperatorSpec) {
	*out = *in
	if in.AttacherNodeSelector != nil {
		in, out := &in.AttacherNodeSelector, &out.AttacherNodeSelector
		*out = make([]KeyVal, len(*in))
		copy(*out, *in)
	}
	if in.ProvisionerNodeSelector != nil {
		in, out := &in.ProvisionerNodeSelector, &out.ProvisionerNodeSelector
		*out = make([]KeyVal, len(*in))
		copy(*out, *in)
	}
	if in.PluginNodeSelector != nil {
		in, out := &in.PluginNodeSelector, &out.PluginNodeSelector
		*out = make([]KeyVal, len(*in))
		copy(*out, *in)
	}
	if in.NodeMapping != nil {
		in, out := &in.NodeMapping, &out.NodeMapping
		*out = make([]NodeMap, len(*in))
		copy(*out, *in)
	}
	if in.Clusters != nil {
		in, out := &in.Clusters, &out.Clusters
		*out = make([]CSIClusterSpec, len(*in))
		for i := range *in {
			(*in)[i].DeepCopyInto(&(*out)[i])
		}
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new CSIScaleOperatorSpec.
func (in *CSIScaleOperatorSpec) DeepCopy() *CSIScaleOperatorSpec {
	if in == nil {
		return nil
	}
	out := new(CSIScaleOperatorSpec)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *CSIScaleOperatorStatus) DeepCopyInto(out *CSIScaleOperatorStatus) {
	*out = *in
	if in.Conditions != nil {
		in, out := &in.Conditions, &out.Conditions
		*out = make([]CSIScaleOperatorCondition, len(*in))
		copy(*out, *in)
	}
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new CSIScaleOperatorStatus.
func (in *CSIScaleOperatorStatus) DeepCopy() *CSIScaleOperatorStatus {
	if in == nil {
		return nil
	}
	out := new(CSIScaleOperatorStatus)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *KeyVal) DeepCopyInto(out *KeyVal) {
	*out = *in
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new KeyVal.
func (in *KeyVal) DeepCopy() *KeyVal {
	if in == nil {
		return nil
	}
	out := new(KeyVal)
	in.DeepCopyInto(out)
	return out
}

// DeepCopyInto is an autogenerated deepcopy function, copying the receiver, writing into out. in must be non-nil.
func (in *NodeMap) DeepCopyInto(out *NodeMap) {
	*out = *in
	return
}

// DeepCopy is an autogenerated deepcopy function, copying the receiver, creating a new NodeMap.
func (in *NodeMap) DeepCopy() *NodeMap {
	if in == nil {
		return nil
	}
	out := new(NodeMap)
	in.DeepCopyInto(out)
	return out
}
