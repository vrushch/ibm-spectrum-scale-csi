# Installing IBM Spectrum Scale Container Storage Interface driver using Operator Lifecycle Manager

This topic describes the procedure for installing IBM Spectrum Scale Container Storage Interface driver using Operator Lifecycle Manager (OLM).

OLM runs by default on Red Hat® OpenShift® Container Platform 4.2 and later releases. For more information, see [Operator Lifecycle Manager workflow and architecture](https://www.ibm.com/links?url=https%3A%2F%2Fdocs.openshift.com%2Fcontainer-platform%2F4.7%2Foperators%2Funderstanding%2Folm%2Folm-understanding-olm.html). OLM is not available by default on Kubernetes, and it is recommended to use CLI-based installation of the IBM Spectrum Scale Container Storage Interface driver on Kubernetes. For more information, see [Installing IBM Spectrum Scale Container Storage Interface driver using CLIs](https://www.ibm.com/docs/en/STXKQY_CSI_SHR/com.ibm.spectrum.scale.csi.v2r20.doc/bl1csi_install_usingops.html#concept_fhm_3mm_rjb). However, if OLM is already installed on the Kubernetes cluster, then use the method that is described here.

Before performing IBM Spectrum Scale Container Storage Interface driver installation, ensure that the prerequisites are met. For more information, see [Performing pre-installation tasks](https://www.ibm.com/docs/en/STXKQY_CSI_SHR/com.ibm.spectrum.scale.csi.v2r20.doc/bl1csi_instal_prereq.html#bl1csi_instal_prereq).

### Steps for Installing IBM Spectrum Scale Container Storage Interface driver using Operator Lifecycle Manager on Openshift and Kubernetes:
1. Login to the Red Hat OpenShift Container Platform/ OKD kubernetes Console.
2. Create Namespace/Project ibm-spectrum-scale-csi-driver
3. From the left panel, click **Operators > OperatorHub**. The OperatorHub page appears.
4. From the Namespace/Project drop-down list, select the Namespace/Project.
5. In the **Filter by keyword** box, type "IBM Spectrum Scale CSI".
6. Click **IBM Spectrum Scale CSI Plugin Operator**. The IBM Spectrum® Scale CSI Plugin Operator page appears.
7. Click Install. The Install Operator page appears.
8. On this page, select the approval strategy (automatic or manual), and click **Install**. The Installed Operators - ready for use page appears, where IBM Spectrum Scale CSI Plugin Operator is listed as successfully installed.
9. On the Installed Operators - ready for use page, click View Operator, and go to the IBM CSI Spectrum Scale Driver tab.
10. Create [Secrets](https://www.ibm.com/docs/en/STXKQY_CSI_SHR/com.ibm.spectrum.scale.csi.v2r20.doc/bl1csi_config_csi_secret.html#concept_pkl_ghh_53b) and [Certificates](https://www.ibm.com/docs/en/STXKQY_CSI_SHR/com.ibm.spectrum.scale.csi.v2r20.doc/bl1csi_config_csi_cert.html#concept_k1l_ljh_53b) as required.
11. Click Create **CSIScale Operator**. The Create CSIScale Operator page appears.
12. On this page, an editor appears, where you can update the custom resource file according to your environment. Choose YAML view for updating custom resource. For more information on custom resource parameters, see [Operator](https://www.ibm.com/docs/en/STXKQY_CSI_SHR/com.ibm.spectrum.scale.csi.v2r20.doc/bl1_csi_scaleoperator_config.html#concept_aqh_zg5_xjb).
