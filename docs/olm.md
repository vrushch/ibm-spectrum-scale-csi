# Installing IBM Spectrum Scale Container Storage Interface driver using Operator Lifecycle Manager

This topic describes the procedure for installing IBM Spectrum Scale Container Storage Interface driver using Operator Lifecycle Manager (OLM).

OLM runs by default on Red Hat® OpenShift® Container Platform 4.2 and later releases. For more information, see [Operator Lifecycle Manager workflow and architecture](https://www.ibm.com/links?url=https%3A%2F%2Fdocs.openshift.com%2Fcontainer-platform%2F4.7%2Foperators%2Funderstanding%2Folm%2Folm-understanding-olm.html). OLM is not available by default on Kubernetes, and it is recommended to use CLI-based installation of the IBM Spectrum Scale Container Storage Interface driver on Kubernetes. For more information, see [Installing IBM Spectrum Scale Container Storage Interface driver using CLIs](https://www.ibm.com/docs/en/STXKQY_CSI_SHR/com.ibm.spectrum.scale.csi.v2r20.doc/bl1csi_install_usingops.html#concept_fhm_3mm_rjb). However, if OLM is already installed on the Kubernetes cluster, then use the method that is described here.

Before performing IBM Spectrum Scale Container Storage Interface driver installation, ensure that the prerequisites are met. For more information, see [Performing pre-installation tasks](https://www.ibm.com/docs/en/STXKQY_CSI_SHR/com.ibm.spectrum.scale.csi.v2r20.doc/bl1csi_instal_prereq.html#bl1csi_instal_prereq).

### Steps for Installing IBM Spectrum Scale Container Storage Interface driver using Operator Lifecycle Manager on Openshift:
1. Create the Operator from the Red Hat OpenShift console by performing the following steps:
2. Log in to the Red Hat OpenShift Container Platform.
3. From the left panel, click Operators > OperatorHub. The OperatorHub page appears.
4. From the Project drop-down list, select the project or create a new project by clicking Create Project.
5. Under All Items, select Storage from the list.
6. In the Filter by keyword box, type "IBM Spectrum Scale CSI".
7. Click IBM Spectrum Scale CSI Plugin Operator. The IBM Spectrum® Scale CSI Plugin Operator page appears.
8. Click Install. The Create Operator Subscription page appears.
9. On this page, select a namespace as that of operator from the available options, select the approval strategy (automatic or manual), and click Subscribe. The Installed Operators page appears, where IBM Spectrum Scale CSI Plugin Operator is listed as successfully installed.
10. On the Installed Operators page, click IBM Spectrum Scale CSI Plugin Operator, and go to the IBM CSI Spectrum Scale Driver tab.
11. Click Create CSIScale Operator. The Create CSIScale Operator page appears.
12. On this page, an editor appears, where you can update the manifest file according to your environment. For more information, see Operator, Secrets, and Certificates.

### Steps for Installing IBM Spectrum Scale Container Storage Interface driver using Operator Lifecycle Manager on Kubernetes:
1. Confirm packagemanifest ibm-spectrum-scale-csi-operator is present. 
```
[root@k8s-master ~]# kubectl get packagemanifest -n olm | grep ibm-spectrum-scale-csi-operator
ibm-spectrum-scale-csi-operator            Community Operators   16h
[root@k8s-master ~]#
```
2. Confirm catalogsource operatorhubio-catalog is present. 
```
[root@k8s-master ~]# kubectl get catalogsource -n olm | grep operatorhubio-catalog
operatorhubio-catalog   Community Operators   grpc   OperatorHub.io   16h
[root@k8s-master ~]#
```
3. Apply following yaml file.
```
apiVersion: v1
kind: Namespace
metadata:
  name: ibm-spectrum-scale-csi-driver
---
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: operatorgroup
  namespace: ibm-spectrum-scale-csi-driver
spec:
  targetNamespaces:
  - ibm-spectrum-scale-csi-driver
---
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: ibm-spectrum-scale-csi-driver
  namespace: ibm-spectrum-scale-csi-driver
spec:
  channel: stable
  name: ibm-spectrum-scale-csi-operator
  source: operatorhubio-catalog
  sourceNamespace: olm
```
```
[root@k8s-master ~]# kubectl apply -f ibm-sectrum-scale-csi-file-olm.yaml
namespace/ibm-spectrum-scale-csi-driver created
operatorgroup.operators.coreos.com/operatorgroup created
subscription.operators.coreos.com/ibm-spectrum-scale-csi-driver created
[root@k8s-master ~]#
```
4. Confirm ibm-spectrum-scale-csi-operator pods are running
```
[root@k8s-master ~]# kubectl get pods -n ibm-spectrum-scale-csi-driver
NAME                                               READY   STATUS    RESTARTS   AGE
ibm-spectrum-scale-csi-operator-75d5f44865-7l7nf   1/1     Running   0          103s
[root@k8s-master ~]#
```
5. Follow **Phase 2: Deploying IBM Spectrum Scale Container Storage Interface driver steps** on [Installing IBM Spectrum Scale Container Storage Interface driver using CLIs](https://www.ibm.com/docs/en/STXKQY_CSI_SHR/com.ibm.spectrum.scale.csi.v2r20.doc/bl1csi_install_usingops.html#concept_fhm_3mm_rjb)
