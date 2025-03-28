    @gather_metrics("number_input")
    def number_input(
        self,
        label: str,
        min_value: Number | None = None,
        max_value: Number | None = None,
        value: Number | Literal["min"] | None = "min",
        step: Number | None = None,
        format: str | None = None,
        key: Key | None = None,
        help: str | None = None,
        on_change: WidgetCallback | None = None,
        args: WidgetArgs | None = None,
        kwargs: WidgetKwargs | None = None,
        *,  # keyword-only arguments:
        placeholder: str | None = None,
        disabled: bool = False,
        label_visibility: LabelVisibility = "visible",
    ) -> Number | None:
        r"""Display a numeric input widget.

        .. note::
            Integer values exceeding +/- ``(1<<53) - 1`` cannot be accurately
            stored or returned by the widget due to serialization contstraints
            between the Python server and JavaScript client. You must handle
            such numbers as floats, leading to a loss in precision.

        Parameters
        ----------
        label : str
            A short label explaining to the user what this input is for.
            The label can optionally contain GitHub-flavored Markdown of the
            following types: Bold, Italics, Strikethroughs, Inline Code, Links,
            and Images. Images display like icons, with a max height equal to
            the font height.

            Unsupported Markdown elements are unwrapped so only their children
            (text contents) render. Display unsupported elements as literal
            characters by backslash-escaping them. E.g.,
            ``"1\. Not an ordered list"``.

            See the ``body`` parameter of |st.markdown|_ for additional,
            supported Markdown directives.

            For accessibility reasons, you should never set an empty label, but
            you can hide it with ``label_visibility`` if needed. In the future,
            we may disallow empty labels by raising an exception.

            .. |st.markdown| replace:: ``st.markdown``
            .. _st.markdown: https://docs.streamlit.io/develop/api-reference/text/st.markdown

        min_value : int, float, or None
            The minimum permitted value.
            If this is ``None`` (default), there will be no minimum for float
            values and a minimum of ``- (1<<53) + 1`` for integer values.

        max_value : int, float, or None
            The maximum permitted value.
            If this is ``None`` (default), there will be no maximum for float
            values and a maximum of ``(1<<53) - 1`` for integer values.

        value : int, float, "min" or None
            The value of this widget when it first renders. If this is
            ``"min"`` (default), the initial value is ``min_value`` unless
            ``min_value`` is ``None``. If ``min_value`` is ``None``, the widget
            initializes with a value of ``0.0`` or ``0``.

            If ``value`` is ``None``, the widget will initialize with no value
            and return ``None`` until the user provides input.

        step : int, float, or None
            The stepping interval.
            Defaults to 1 if the value is an int, 0.01 otherwise.
            If the value is not specified, the format parameter will be used.

        format : str or None
            A printf-style format string controlling how the interface should
            display numbers. The output must be purely numeric. This does not
            impact the return value of the widget. For more information about
            the formatting specification, see `sprintf.js
            <https://github.com/alexei/sprintf.js?tab=readme-ov-file#format-specification>`_.

            For example, ``format="%0.1f"`` adjusts the displayed decimal
            precision to only show one digit after the decimal.

        key : str or int
            An optional string or integer to use as the unique key for the widget.
            If this is omitted, a key will be generated for the widget
            based on its content. No two widgets may have the same key.

        help : str or None
            A tooltip that gets displayed next to the widget label. Streamlit
            only displays the tooltip when ``label_visibility="visible"``. If
            this is ``None`` (default), no tooltip is displayed.

            The tooltip can optionally contain GitHub-flavored Markdown,
            including the Markdown directives described in the ``body``
            parameter of ``st.markdown``.

        on_change : callable
            An optional callback invoked when this number_input's value changes.

        args : tuple
            An optional tuple of args to pass to the callback.

        kwargs : dict
            An optional dict of kwargs to pass to the callback.

        placeholder : str or None
            An optional string displayed when the number input is empty.
            If None, no placeholder is displayed.

        disabled : bool
            An optional boolean that disables the number input if set to
            ``True``. The default is ``False``.

        label_visibility : "visible", "hidden", or "collapsed"
            The visibility of the label. The default is ``"visible"``. If this
            is ``"hidden"``, Streamlit displays an empty spacer instead of the
            label, which can help keep the widget alligned with other widgets.
            If this is ``"collapsed"``, Streamlit displays no label or spacer.

        Returns
        -------
        int or float or None
            The current value of the numeric input widget or ``None`` if the widget
            is empty. The return type will match the data type of the value parameter.

        Example
        -------
        >>> import streamlit as st
        >>>
        >>> number = st.number_input("Insert a number")
        >>> st.write("The current number is ", number)

        .. output::
           https://doc-number-input.streamlit.app/
           height: 260px

        To initialize an empty number input, use ``None`` as the value:

        >>> import streamlit as st
        >>>
        >>> number = st.number_input(
        ...     "Insert a number", value=None, placeholder="Type a number..."
        ... )
        >>> st.write("The current number is ", number)

        .. output::
           https://doc-number-input-empty.streamlit.app/
           height: 260px

        """
        ctx = get_script_run_ctx()
        return self._number_input(
            label=label,
            min_value=min_value,
            max_value=max_value,
            value=value,
            step=step,
            format=format,
            key=key,
            help=help,
            on_change=on_change,
            args=args,
            kwargs=kwargs,
            placeholder=placeholder,
            disabled=disabled,
            label_visibility=label_visibility,
            ctx=ctx,
        )
