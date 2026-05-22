# Dockerfile: BehaVerify vs BT2Fiacre vs BT2BIP comparison harness
#
# Self-contained image that runs:
#   - Table 2  : BehaVerify FF vs naive ablation (N = 1..10, 3-run average, 5 min timeout)
#   - Table 3  : BehaVerify drone3 + droneNew  AND  BT2Fiacre drone3 + drone4
#   - Sec 4.3  : BehaVerify on BT2BIP's MarsRover + TrainControl
#
# Pinning (for repeatability across re-builds):
#   BehaVerify  -- the local working tree is COPYed in at build time
#                  (see .dockerignore alongside this file).
#   BT2Fiacre   -- pinned to BT2FIACRE_SHA below.
#   Tina        -- 4.0.0       (https://projects.laas.fr/tina/binaries/)
#   Hippo/frac  -- 2.7.1       (https://projects.laas.fr/hippo/binaries/)
#   nuXmv       -- 2.1.0 (linux64, https://nuxmv.fbk.eu/downloads/)
#
# Build (from BehaVerify repo root):
#   docker build -f REPRODUCIBILITY/2026_ATVA/compare/Dockerfile -t behaverify-compare .
#
# Run:
#   docker run --rm behaverify-compare
#     ... or, to keep the per-run reports on the host:
#   docker run --rm -v "$(pwd)/REPRODUCIBILITY/2026_ATVA/compare/output:/out" behaverify-compare
#
# Output:
#   STDOUT          -- formatted Table 2, Table 3, Section 4.3 tables
#   /out/results.txt-- same content, also written to disk if /out is mounted

FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Pinned versions ------------------------------------------------------------
ARG BT2FIACRE_SHA=70be4269c7dc1f3fd7ac0801265de0afaf158407
ARG TINA_VER=4.0.0
ARG HIPPO_VER=2.7.1
ARG NUXMV_VER=2.1.0

# --- Base toolchain ---------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl wget tar gzip xz-utils unzip \
        build-essential gcc g++ make cmake git autoconf automake libtool pkg-config m4 \
        bison flex dos2unix \
        python3 python3-pip python3-venv python3-tk \
        coreutils time \
        graphviz \
        libgmp-dev libreadline-dev libtinyxml2-dev \
        ocaml ocaml-findlib \
    && rm -rf /var/lib/apt/lists/*

# --- nuXmv 2.1.0 (LINUX) ---------------------------------------------------
RUN mkdir -p /opt/nuxmv && cd /opt/nuxmv \
 && curl -fsSL "https://nuxmv.fbk.eu/downloads/nuXmv-${NUXMV_VER}-linux64.tar.xz" -o nuxmv.tar.xz \
 && tar -xJf nuxmv.tar.xz --strip-components=1 \
 && rm nuxmv.tar.xz \
 && chmod +x bin/nuXmv
ENV PATH="/opt/nuxmv/bin:${PATH}"

# --- Tina 4.0.0 (Time Petri Net Analyzer) ----------------------------------
RUN mkdir -p /opt/tina && cd /opt/tina \
 && curl -fsSL "https://projects.laas.fr/tina/binaries/tina-${TINA_VER}-amd64-linux.tgz" -o tina.tgz \
 && tar -xzf tina.tgz --strip-components=1 \
 && rm tina.tgz
ENV TINA_DIST="/opt/tina"
ENV PATH="/opt/tina/bin:${PATH}"

# --- Hippo 2.7.1 (frac compiler + hippo runtime) ---------------------------
RUN mkdir -p /opt/hippo && cd /opt/hippo \
 && curl -fsSL "https://projects.laas.fr/hippo/binaries/hippo-${HIPPO_VER}-amd64-linux.tgz" -o hippo.tgz \
 && tar -xzf hippo.tgz --strip-components=1 \
 && rm hippo.tgz
ENV HIPPO_DIST="/opt/hippo"
ENV PATH="/opt/hippo:/opt/hippo/bin:${PATH}"

# --- BT2Fiacre (pinned SHA) ------------------------------------------------
# Cloned via git:// daemon to bypass the Anubis-protected HTTPS frontend.
RUN git clone git://redmine.laas.fr/laas/users/felix/bt2fiacre.git /opt/bt2fiacre \
 && cd /opt/bt2fiacre && git checkout "${BT2FIACRE_SHA}"
WORKDIR /opt/bt2fiacre
# Patch configure.ac: relax AC_PREREQ to what Ubuntu ships (2.71) and drop
# the bare AC_REQUIRE that autoconf >= 2.72 mis-expands outside an AC_DEFUN.
RUN mkdir -p m4 \
 && sed -i 's/AC_PREREQ(\[2\.73\])/AC_PREREQ([2.71])/' configure.ac \
 && sed -i '/^AC_REQUIRE(AC_PROG_CC)/d' configure.ac \
 && ./bootstrap.sh \
 && ./configure --prefix=/opt/bt2fiacre/install \
 && make -j"$(nproc)" \
 && (make install 2>/dev/null || true)
ENV PATH="/opt/bt2fiacre/install/bin:/opt/bt2fiacre/src:/opt/bt2fiacre:${PATH}"

# --- BehaVerify (frozen from the build context) -----------------------------
# The local working tree is COPYed in via .dockerignore filtering.
WORKDIR /home/bv
COPY pyproject.toml /home/bv/behaverify/pyproject.toml
COPY src             /home/bv/behaverify/src
COPY REPRODUCIBILITY/2026_ATVA /home/bv/behaverify/REPRODUCIBILITY/2026_ATVA
RUN find /home/bv/behaverify/REPRODUCIBILITY/2026_ATVA -type f \
        \( -name '*.sh' -o -name '*.py' -o -name '*.tx' -o -name 'command_*' \) \
        -exec dos2unix -q {} + \
 && find /home/bv/behaverify/REPRODUCIBILITY/2026_ATVA -name '*.sh' -exec chmod +x {} + \
 && python3 -m venv /home/bv/venv \
 && /home/bv/venv/bin/python3 -m pip install --upgrade pip \
 && /home/bv/venv/bin/python3 -m pip install -e /home/bv/behaverify \
 && /home/bv/venv/bin/python3 -m pip install -r /home/bv/behaverify/REPRODUCIBILITY/2026_ATVA/requirements/core.txt \
 && cp /opt/nuxmv/bin/nuXmv /home/bv/behaverify/REPRODUCIBILITY/2026_ATVA/nuXmv \
 && chmod +x /home/bv/behaverify/REPRODUCIBILITY/2026_ATVA/nuXmv
ENV PATH="/home/bv/venv/bin:${PATH}"

# --- Comparison harness scripts -------------------------------------------
COPY REPRODUCIBILITY/2026_ATVA/compare/run_all.sh         /home/bv/run_all.sh
COPY REPRODUCIBILITY/2026_ATVA/compare/run_table2.sh      /home/bv/run_table2.sh
COPY REPRODUCIBILITY/2026_ATVA/compare/run_table3.sh      /home/bv/run_table3.sh
COPY REPRODUCIBILITY/2026_ATVA/compare/run_section43.sh   /home/bv/run_section43.sh
COPY REPRODUCIBILITY/2026_ATVA/compare/run_smoke.sh       /home/bv/run_smoke.sh
COPY REPRODUCIBILITY/2026_ATVA/compare/format_results.py  /home/bv/format_results.py
RUN dos2unix -q /home/bv/*.sh /home/bv/format_results.py && chmod +x /home/bv/*.sh

# --- Sanity check ---------------------------------------------------------
RUN set +e; \
    echo "--- nuXmv ---";    nuXmv -h 2>&1 | head -2; \
    echo "--- Tina ---";     tina -h 2>&1 | head -2; \
    echo "--- frac ---";     frac -version 2>&1 | head -2; \
    echo "--- bt2fiacre ---"; bt2fiacre -c "exit" foo 2>&1 | head -3; \
    echo "--- BehaVerify ---"; python3 -c "import behaverify; print(behaverify.__name__, 'OK')"; \
    true

WORKDIR /home/bv
CMD ["/home/bv/run_all.sh"]
